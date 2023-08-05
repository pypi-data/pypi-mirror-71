from __future__ import annotations

from math import log
from typing import List, Type

from hmmer_reader import HMMERModel
from imm import (
    Interval,
    MuteState,
    Path,
    Sequence,
    SequenceABC,
    lprob_add,
    lprob_normalize,
    lprob_zero,
)
from nmm import (
    AminoAlphabet,
    AminoTable,
    BaseAlphabet,
    BaseTable,
    CodonProb,
    CodonTable,
    FrameState,
    GeneticCode,
    codon_iter,
)

from iseq.model import EntryDistr, Transitions
from iseq.profile import Profile

from ._fragment import ProteinFragment
from .typing import (
    ProteinAltModel,
    ProteinNode,
    ProteinNullModel,
    ProteinSearchResults,
    ProteinSpecialNode,
    ProteinStep,
)

__all__ = ["ProteinProfile", "create_profile"]


class ProteinProfile(Profile[BaseAlphabet, FrameState]):
    @classmethod
    def create(
        cls: Type[ProteinProfile],
        factory: ProteinStateFactory,
        null_aminot: AminoTable,
        core_nodes: List[ProteinNode],
        core_trans: List[Transitions],
    ) -> ProteinProfile:

        base_alphabet = factory.genetic_code.base_alphabet

        R = factory.create(b"R", null_aminot)
        null_model = ProteinNullModel.create(R)

        special_node = ProteinSpecialNode(
            S=MuteState.create(b"S", base_alphabet),
            N=factory.create(b"N", null_aminot),
            B=MuteState.create(b"B", base_alphabet),
            E=MuteState.create(b"E", base_alphabet),
            J=factory.create(b"J", null_aminot),
            C=factory.create(b"C", null_aminot),
            T=MuteState.create(b"T", base_alphabet),
        )

        alt_model = ProteinAltModel.create(
            special_node, core_nodes, core_trans, EntryDistr.UNIFORM,
        )
        # alt_model.set_fragment_length(self._special_transitions)
        return cls(base_alphabet, null_model, alt_model, False)

    @classmethod
    def create2(
        cls: Type[ProteinProfile],
        alphabet: BaseAlphabet,
        null_model: ProteinNullModel,
        alt_model: ProteinAltModel,
        hmmer3_compat: bool,
    ):
        return cls(alphabet, null_model, alt_model, hmmer3_compat)

    @property
    def null_model(self) -> ProteinNullModel:
        return self._null_model

    @property
    def alt_model(self) -> ProteinAltModel:
        return self._alt_model

    def search(
        self, sequence: SequenceABC[BaseAlphabet], window_length: int = 0
    ) -> ProteinSearchResults:

        # special_trans = self._get_target_length_model(len(sequence))
        # self._alt_model.set_special_transitions(special_trans)
        # self._null_model.set_special_transitions(special_trans)

        # alt_results = self.alt_model.viterbi(sequence, window_length)
        self._set_target_length_model(len(sequence))
        if window_length == -1:
            window_length = 2 * 3 * self._alt_model.core_length
        alt_results = self._alt_model.viterbi(sequence, window_length)

        def create_fragment(
            seq: SequenceABC[BaseAlphabet], path: Path[ProteinStep], homologous: bool
        ):
            return ProteinFragment(seq, path, homologous)

        search_results = ProteinSearchResults(sequence, create_fragment)

        for alt_result in alt_results:
            subseq = alt_result.sequence
            # TODO: temporary fix for reading from binary file
            # and consequently alt and null model having different alphabets
            s = Sequence.create(bytes(subseq), self._null_model.hmm.alphabet)
            viterbi_score0 = self._null_model.likelihood(s)
            # viterbi_score0 = self._null_model.likelihood(subseq)
            viterbi_score1 = alt_result.loglikelihood
            score = viterbi_score1 - viterbi_score0
            window = Interval(subseq.start, subseq.start + len(subseq))
            search_results.append(
                score, window, alt_result.path, viterbi_score1, viterbi_score0
            )

        return search_results


def create_profile(
    reader: HMMERModel, base_abc: BaseAlphabet, epsilon: float = 0.1
) -> ProteinProfile:

    amino_abc = AminoAlphabet.create(reader.alphabet.encode(), b"X")

    lprobs = lprob_normalize(list(reader.insert(0).values())).tolist()
    null_aminot = AminoTable.create(amino_abc, lprobs)
    factory = ProteinStateFactory(GeneticCode(base_abc, amino_abc), epsilon)

    nodes: List[ProteinNode] = []
    for m in range(1, reader.M + 1):
        lprobs = lprob_normalize(list(reader.match(m).values())).tolist()
        M = factory.create(f"M{m}".encode(), AminoTable.create(amino_abc, lprobs))

        lprobs = lprob_normalize(list(reader.insert(m).values())).tolist()
        I = factory.create(f"I{m}".encode(), AminoTable.create(amino_abc, lprobs))

        D = MuteState.create(f"D{m}".encode(), base_abc)

        nodes.append(ProteinNode(M, I, D))

    trans: List[Transitions] = []
    for m in range(0, reader.M + 1):
        t = Transitions(**reader.trans(m))
        t.normalize()
        trans.append(t)

    return ProteinProfile.create(factory, null_aminot, nodes, trans)


class ProteinStateFactory:
    def __init__(
        self, gcode: GeneticCode, epsilon: float,
    ):
        self._gcode = gcode
        self._epsilon = epsilon

    def create(self, name: bytes, aminot: AminoTable) -> FrameState:
        codonp = _create_codon_prob(aminot, self._gcode)
        baset = _create_base_table(codonp)
        codont = CodonTable.create(codonp)
        return FrameState.create(name, baset, codont, self._epsilon)

    @property
    def genetic_code(self) -> GeneticCode:
        return self._gcode

    @property
    def epsilon(self) -> float:
        return self._epsilon


def _create_base_table(codonp: CodonProb):
    base_abc = codonp.alphabet
    base_lprob = {base: lprob_zero() for base in base_abc.symbols}
    norm = log(3)
    for codon in codon_iter(base_abc):
        lprob = codonp.get_lprob(codon)
        triplet = codon.symbols

        base_lprob[triplet[0]] = lprob_add(base_lprob[triplet[0]], lprob - norm)
        base_lprob[triplet[1]] = lprob_add(base_lprob[triplet[1]], lprob - norm)
        base_lprob[triplet[2]] = lprob_add(base_lprob[triplet[2]], lprob - norm)

    return BaseTable.create(base_abc, [base_lprob[base] for base in base_abc.symbols])


def _create_codon_prob(aminot: AminoTable, gencode: GeneticCode) -> CodonProb:
    codonp = CodonProb.create(gencode.base_alphabet)

    codon_lprobs = []
    lprob_norm = lprob_zero()
    for i in range(len(aminot.alphabet.symbols)):
        aa = aminot.alphabet.symbols[i : i + 1]
        lprob = aminot.lprob(aa)

        codons = gencode.codons(aa)
        if len(codons) == 0:
            continue

        norm = log(len(codons))
        for codon in codons:
            codon_lprobs.append((codon, lprob - norm))
            lprob_norm = lprob_add(lprob_norm, codon_lprobs[-1][1])

    for codon, lprob in codon_lprobs:
        codonp.set_lprob(codon, lprob - lprob_norm)

    return codonp
