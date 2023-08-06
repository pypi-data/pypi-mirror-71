import os
import sys
import shutil
import pkg_resources
from tqdm import tqdm
import multiprocessing as mp
from abc import ABC, abstractmethod
from multiprocessing.queues import Queue as mpQueue
from collections import defaultdict, namedtuple, OrderedDict

import numpy as np


# TODO move these values into model specific files as they may change from
# model to model. Need to create script to automate HET_FACTOR optimization
# process first
# Also potentially use sepatate insertion and deletion factor
# determine necessity from larger validation run
DEFAULT_SNV_HET_FACTOR = 1.0
DEFAULT_INDEL_HET_FACTOR = 1.0

DEFAULT_EDGE_BUFFER = 30
CONTEXT_MAX_DIST = 5
DEFAULT_MAX_INDEL_SIZE = 50
DEFUALT_MAX_VAR_CNTXTS = 16
DEFAULT_SNV_CONTEXT = 15
DEFAULT_INDEL_CONTEXT = 30
DEFAULT_VAR_CONTEXT_BASES = [DEFAULT_SNV_CONTEXT, DEFAULT_INDEL_CONTEXT]
DEFAULT_MOD_CONTEXT = 15
DEFAULT_CONTEXT_MIN_ALT_PROB = 0.0
MOD_BIN_THRESH_NAME = 'binary_threshold'
MOD_EM_NAME = 'expectation_maximization'
MOD_AGG_METHOD_NAMES = set((MOD_BIN_THRESH_NAME, MOD_EM_NAME))
DEFAULT_MOD_BINARY_THRESH = 0.8

MED_NORM_FACTOR = 1.4826

ALPHABET = 'ACGT'
# set RNA alphabet for use in reading guppy posterior output
# requiring assumed canonical alphabet
RNA_ALPHABET = 'ACGU'
VALID_ALPHABETS = [ALPHABET, RNA_ALPHABET]
COMP_BASES = dict(zip(map(ord, 'ACGT'), map(ord, 'TGCA')))
NP_COMP_BASES = np.array([3, 2, 1, 0], dtype=np.uintp)
SEQ_MIN = np.array(['A'], dtype='S1').view(np.uint8)[0]
SEQ_TO_INT_ARR = np.full(26, -1, dtype=np.uintp)
SEQ_TO_INT_ARR[0] = 0
SEQ_TO_INT_ARR[2] = 1
SEQ_TO_INT_ARR[6] = 2
SEQ_TO_INT_ARR[19] = 3
SINGLE_LETTER_CODE = {
    'A': 'A', 'C': 'C', 'G': 'G', 'T': 'T', 'B': 'CGT', 'D': 'AGT', 'H': 'ACT',
    'K': 'GT', 'M': 'AC', 'N': 'ACGT', 'R': 'AG', 'S': 'CG', 'V': 'ACG',
    'W': 'AT', 'Y': 'CT'}
PHRED_BASE = 33

CHAN_INFO_CHANNEL_SLOT = 'channel_number'
CHAN_INFO_OFFSET = 'offset'
CHAN_INFO_RANGE = 'range'
CHAN_INFO_DIGI = 'digitisation'
CHAN_INFO_SAMP_RATE = 'sampling_rate'

_MAX_QUEUE_SIZE = 10000

# allow 64GB for memory mapped sqlite file access
MEMORY_MAP_LIMIT = 64000000000
DEFAULT_VAR_DATABASE_TIMEOUT = 5
DEFAULT_MOD_DATABASE_TIMEOUT = 5
# default cache size in kilobytes
SQLITE_CACHE_SIZE = 10000
SQLITE_PAGE_SIZE = 65536
SQLITE_MAX_PAGE_COUNT = 2147483646
SQLITE_THREADS = 8

# VCF spec text
MIN_GL_VALUE = -999
MAX_PL_VALUE = 999
VCF_VERSION_MI = 'fileformat=VCFv{}'
FILE_DATE_MI = 'fileDate={}'
SOURCE_MI = 'source=ont-megalodon.v{}'
REF_MI = "reference={}"
CONTIG_MI = "contig=<ID={},length={}>"
STRAND_FIELD_NAME = 'STRAND'

# outputs specification
BC_NAME = 'basecalls'
BC_OUT_FMTS = ('fastq', 'fasta')
SEQ_SUMM_NAME = 'seq_summary'
BC_MODS_NAME = 'mod_basecalls'
MAP_NAME = 'mappings'
MAP_SUMM_NAME = 'mappings_summary'
MAP_OUT_BAM = 'bam'
MAP_OUT_CRAM = 'cram'
MAP_OUT_SAM = 'sam'
MAP_OUT_FMTS = (MAP_OUT_BAM, MAP_OUT_CRAM, MAP_OUT_SAM)
MAP_OUT_WRITE_MODES = {MAP_OUT_BAM: 'wb', MAP_OUT_CRAM: 'wc', MAP_OUT_SAM: 'w'}
PR_VAR_NAME = 'per_read_variants'
PR_VAR_TXT_NAME = 'per_read_variants_text'
VAR_MAP_NAME = 'variant_mappings'
VAR_NAME = 'variants'
PR_MOD_NAME = 'per_read_mods'
PR_MOD_TXT_NAME = 'per_read_mods_text'
MOD_MAP_NAME = 'mod_mappings'
MOD_NAME = 'mods'
SIG_MAP_NAME = 'signal_mappings'
PR_REF_NAME = 'per_read_refs'
OUTPUT_FNS = {
    BC_NAME: 'basecalls',
    SEQ_SUMM_NAME: 'sequencing_summary.txt',
    BC_MODS_NAME: 'basecalls.modified_base_scores.hdf5',
    MAP_NAME: 'mappings',
    MAP_SUMM_NAME: 'mappings.summary.txt',
    PR_VAR_NAME: 'per_read_variant_calls.db',
    PR_VAR_TXT_NAME: 'per_read_variant_calls.txt',
    VAR_NAME: 'variants.vcf',
    VAR_MAP_NAME: 'variant_mappings',
    PR_MOD_NAME: 'per_read_modified_base_calls.db',
    PR_MOD_TXT_NAME: 'per_read_modified_base_calls.txt',
    MOD_MAP_NAME: 'mod_mappings',
    MOD_NAME: 'modified_bases',
    SIG_MAP_NAME: 'signal_mappings.hdf5',
    PR_REF_NAME: 'per_read_references.fasta'
}
LOG_FILENAME = 'log.txt'
# outputs to be selected with command line --outputs argument
OUTPUT_DESCS = OrderedDict([
    (BC_NAME, 'Called bases (FASTA/Q)'),
    (BC_MODS_NAME, 'Basecall-anchored modified base scores (HDF5)'),
    (MAP_NAME, 'Mapped reads (BAM/CRAM/SAM)'),
    (PR_VAR_NAME, 'Per-read, per-site sequence variant scores database'),
    (VAR_NAME, 'Sample-level aggregated sequence variant calls (VCF)'),
    (VAR_MAP_NAME, 'Per-read mappings annotated with variant calls'),
    (PR_MOD_NAME, 'Per-read, per-site modified base scores database'),
    (MOD_NAME, 'Sample-level aggregated modified base calls (modVCF)'),
    (MOD_MAP_NAME, 'Per-read mappings annotated with modified base calls'),
    (SIG_MAP_NAME, 'Signal mappings for taiyaki model training (HDF5)'),
    (PR_REF_NAME, 'Per-read reference sequence for model training (FASTA)')
])

# output formats for modified bases and file extensions
MOD_BEDMETHYL_NAME = 'bedmethyl'
MOD_VCF_NAME = 'modvcf'
MOD_WIG_NAME = 'wiggle'
MOD_OUTPUT_FMTS = {
    MOD_BEDMETHYL_NAME: 'bedMethyl',
    MOD_VCF_NAME: 'modVcf',
    MOD_WIG_NAME: 'wig'
}
MOD_OUTPUT_EXTNS = {
    MOD_BEDMETHYL_NAME: 'bed',
    MOD_VCF_NAME: 'vcf',
    MOD_WIG_NAME: 'wig'
}

ALIGN_OUTPUTS = set((MAP_NAME, PR_REF_NAME, SIG_MAP_NAME,
                     PR_VAR_NAME, VAR_NAME, VAR_MAP_NAME,
                     PR_MOD_NAME, MOD_NAME, MOD_MAP_NAME))
GETTER_PROC = namedtuple('getter_proc', ('queue', 'proc', 'conn'))

REF_OUT_INFO = namedtuple('ref_out_info', (
    'pct_idnt', 'pct_cov', 'min_len', 'max_len', 'alphabet',
    'collapse_alphabet', 'mod_long_names', 'annotate_mods', 'annotate_vars',
    'output_sig_maps', 'output_pr_refs', 'ref_mods_all_motifs'))

# directory names define model preset string
# currently only one model trained
MODEL_DATA_DIR_NAME = 'model_data'
VAR_CALIBRATION_FN = 'megalodon_variant_calibration.npz'
MOD_CALIBRATION_FN = 'megalodon_mod_calibration.npz'
DEFAULT_CALIB_SMOOTH_BW = 0.8
DEFAULT_CALIB_SMOOTH_MAX = 200
DEFAULT_CALIB_SMOOTH_NVALS = 5001
DEFAULT_CALIB_MIN_DENSITY = 5e-8
DEFAULT_CALIB_DIFF_EPS = 1e-6
DEFAULT_CALIB_LLR_CLIP_BUFFER = 1

SEQ_SUMM_INFO = namedtuple('seq_summ_info', (
    'filename', 'read_id', 'run_id', 'batch_id', 'channel', 'mux',
    'start_time', 'duration', 'num_events', 'passes_filtering',
    'template_start', 'num_events_template', 'template_duration',
    'sequence_length_template', 'mean_qscore_template',
    'strand_score_template', 'median_template', 'mad_template',
    'scaling_median_template', 'scaling_mad_template'))
# set default value of None for ref, alts, ref_start and strand;
# false for has_context_base
SEQ_SUMM_INFO.__new__.__defaults__ = tuple(['NA', ] * 11)

# default guppy settings
DEFAULT_GUPPY_SERVER_PATH = './ont-guppy/bin/guppy_basecall_server'
DEFAULT_GUPPY_CFG = 'dna_r9.4.1_450bps_modbases_dam-dcm-cpg_hac.cfg'
DEFAULT_GUPPY_TIMEOUT = 5.0

TRUE_TEXT_VALUES = set(('y', 'yes', 't', 'true', 'on', '1'))
FALSE_TEXT_VALUES = set(('n', 'no', 'f', 'false', 'off', '0'))


class MegaError(Exception):
    """ Custom megalodon error for more graceful error handling
    """
    pass


####################
# Helper Functions #
####################

def nstate_to_nbase(nstate):
    return int(np.sqrt(0.25 + (0.5 * nstate)) - 0.5)


def comp(seq):
    return seq.translate(COMP_BASES)


def revcomp(seq):
    return seq.translate(COMP_BASES)[::-1]


def comp_np(np_seq):
    return NP_COMP_BASES[np_seq]


def revcomp_np(np_seq):
    return NP_COMP_BASES[np_seq][::-1]


def seq_to_int(seq, error_on_invalid=True):
    try:
        np_seq = SEQ_TO_INT_ARR[
            np.array(list(seq), dtype='c').view(np.uint8) - SEQ_MIN]
    except IndexError:
        if error_on_invalid:
            raise MegaError('Invalid character in sequence')
        else:
            # use slower string find method to convert seq with
            # invalid characters
            np_seq = np.array([ALPHABET.find(b) for b in seq], dtype=np.uintp)
    # if error_on_invalid and np_seq.shape[0] > 0 and np_seq.max() >= 4:
    #    raise MegaError('Invalid character in sequence')
    return np_seq


def int_to_seq(np_seq, alphabet=ALPHABET):
    if np_seq.shape[0] == 0:
        return ''
    if np_seq.max() >= len(alphabet):
        raise MegaError('Invalid character in sequence')
    return ''.join(alphabet[b] for b in np_seq)


def get_mean_q_score(read_q):
    """ Extract mean q-score from FASTQ quality string
    """
    return np.mean([q_val - PHRED_BASE
                    for q_val in read_q.encode('ASCII')])


def rolling_window(a, size):
    shape = a.shape[:-1] + (a.shape[-1] - size + 1, size)
    strides = a.strides + (a. strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def log_prob_to_phred(log_prob, ignore_np_divide=True):
    if ignore_np_divide:
        with np.errstate(divide='ignore'):
            return -10 * np.log10(1 - np.exp(log_prob))
    return -10 * np.log10(1 - np.exp(log_prob))


def extract_seq_summary_info(read):
    """ Extract non-basecalling sequencing summary information from
    ont_fast5_api read object
    """
    try:
        fn = read.filename
        read_id = read.read_id
        channel_info = read.get_channel_info()
        read_info = read.status.read_info[0]
        run_id = read.get_run_id()
        try:
            run_id = run_id.decode()
        except AttributeError:
            pass
        batch_id = 'NA'
        chan = channel_info[CHAN_INFO_CHANNEL_SLOT]
        mux = read_info.start_mux
        samp_rate = channel_info[CHAN_INFO_SAMP_RATE]
        start_time = '{:.6f}'.format(read_info.start_time / samp_rate)
        dur = '{:.6f}'.format(read_info.duration / samp_rate)
        num_events = str(read_info.event_data_count
                         if read_info.has_event_data else 'NA')
    except Exception:
        # if anything goes wrong set all avlues to NA
        fn = read_id = run_id = batch_id = chan = mux = start_time = dur = \
                       num_events = 'NA'
    return SEQ_SUMM_INFO(
        filename=fn, read_id=read_id, run_id=run_id, batch_id=batch_id,
        channel=chan, mux=mux, start_time=start_time, duration=dur,
        num_events=num_events)


#######################
# Filename Extraction #
#######################

def resolve_path(fn_path):
    """Helper function to resolve relative and linked paths that might
    give other packages problems.
    """
    return os.path.realpath(os.path.expanduser(fn_path))


def get_megalodon_fn(out_dir, out_type):
    return os.path.join(out_dir, OUTPUT_FNS[out_type])


def add_fn_suffix(fn, suffix):
    if suffix is not None:
        base_fn, fn_ext = os.path.splitext(fn)
        fn = base_fn + '.' + suffix + fn_ext
    return fn


def mkdir(out_dir, overwrite):
    if os.path.exists(out_dir):
        if not overwrite:
            raise MegaError(
                '--output-directory exists and --overwrite is not set.')
        if os.path.isfile(out_dir) or os.path.islink(out_dir):
            os.remove(out_dir)
        else:
            shutil.rmtree(out_dir)
    os.mkdir(out_dir)


def prep_out_fn(out_fn, overwrite):
    if os.path.exists(out_fn):
        if overwrite:
            os.remove(out_fn)
        else:
            raise NotImplementedError(
                'ERROR: Output filename exists and --overwrite not set.')
    try:
        open(out_fn, 'w').close()
        os.remove(out_fn)
    except Exception as e:
        sys.stderr.write(
            '*' * 60 + '\nERROR: Attempt to write to output filename ' +
            'location failed with the following error.\n' + '*' * 60 + '\n\n')
        raise e


############################
# Calibration File Loading #
############################

def get_var_calibration_fn(
        guppy_config=None, var_calib_fn=None, disable_var_calib=False):
    if disable_var_calib:
        return None
    if var_calib_fn is not None:
        var_calib_fn = resolve_path(var_calib_fn)
        if not os.path.exists(var_calib_fn):
            raise MegaError(
                'Sequence variants calibration file not found: {}'.format(
                    var_calib_fn))
        return var_calib_fn
    if guppy_config is not None:
        guppy_calib_fn = resolve_path(pkg_resources.resource_filename(
            'megalodon', os.path.join(
                MODEL_DATA_DIR_NAME, guppy_config, VAR_CALIBRATION_FN)))
        if not os.path.exists(guppy_calib_fn):
            raise MegaError(
                'No default sequence variant calibration file found for ' +
                'guppy config: {}'.format(guppy_config))
        return guppy_calib_fn
    raise MegaError('No valid sequence variant calibration specified.')


def get_mod_calibration_fn(
        guppy_config=None, mod_calib_fn=None, disable_mod_calib=False):
    if disable_mod_calib:
        return None
    if mod_calib_fn is not None:
        mod_calib_fn = resolve_path(mod_calib_fn)
        if not os.path.exists(mod_calib_fn):
            raise MegaError(
                'Modified base calibration file not found: {}'.format(
                    mod_calib_fn))
        return mod_calib_fn
    if guppy_config is not None:
        guppy_calib_fn = resolve_path(pkg_resources.resource_filename(
            'megalodon', os.path.join(
                MODEL_DATA_DIR_NAME, guppy_config, MOD_CALIBRATION_FN)))
        if not os.path.exists(guppy_calib_fn):
            raise MegaError(
                'No default modified base calibration file found for guppy ' +
                'config: {}'.format(guppy_config))
        return guppy_calib_fn
    raise MegaError('No valid modified base calibration specified.')


def get_supported_configs_message():
    configs = os.listdir(resolve_path(pkg_resources.resource_filename(
        'megalodon', MODEL_DATA_DIR_NAME)))
    if len(configs) == 0:
        return ('No guppy config calibration files found. Check that ' +
                'megalodon installation is valid.\n')
    out_msg = ('Megalodon support for guppy configs (basecalling and ' +
               'mapping supported for flip-flop configs):\n' +
               'Variant Support    Modbase Support    Config\n')
    for config in configs:
        config_files = os.listdir(resolve_path(
            pkg_resources.resource_filename('megalodon', os.path.join(
                MODEL_DATA_DIR_NAME, config))))
        out_msg += 'X' + ' ' * 18 if VAR_CALIBRATION_FN in config_files else \
                   ' ' * 19
        out_msg += 'X' + ' ' * 18 if MOD_CALIBRATION_FN in config_files else \
                   ' ' * 19
        out_msg += config + '\n'
    return out_msg


###########################
# Multi-processing Helper #
###########################

class CountingMPQueue(mpQueue):
    """ Minimal version of multiprocessing queue maintaining a queue size
    counter
    """
    def __init__(self, **kwargs):
        super().__init__(ctx=mp.get_context(), **kwargs)
        self.size = mp.Value('i', 0)
        self.maxsize = None
        if 'maxsize' in kwargs:
            self.maxsize = kwargs['maxsize']

    def put(self, *args, **kwargs):
        super().put(*args, **kwargs)
        with self.size.get_lock():
            self.size.value += 1

    def get(self, *args, **kwargs):
        rval = super().get(*args, **kwargs)
        with self.size.get_lock():
            self.size.value -= 1
        return rval

    def qsize(self):
        qsize = max(0, self.size.value)
        if self.maxsize is not None:
            return min(self.maxsize, qsize)
        return qsize

    def empty(self):
        return self.qsize() <= 0


def create_getter_q(getter_func, args, max_size=_MAX_QUEUE_SIZE):
    if max_size is None:
        q = CountingMPQueue()
    else:
        q = CountingMPQueue(maxsize=max_size)
    main_conn, conn = mp.Pipe()
    p = mp.Process(target=getter_func, daemon=True, args=(q, conn, *args))
    p.start()
    return GETTER_PROC(q, p, main_conn)


########################
# Stat Aggregation ABC #
########################

class AbstractAggregationClass(ABC):
    @abstractmethod
    def iter_uniq(self):
        return

    @abstractmethod
    def num_uniq(self):
        return


#####################
# Signal Extraction #
#####################

def med_mad(data, factor=None, axis=None, keepdims=False):
    """Compute the Median Absolute Deviation, i.e., the median
    of the absolute deviations from the median, and the median

    :param data: A :class:`ndarray` object
    :param factor: Factor to scale MAD by. Default (None) is to be consistent
    with the standard deviation of a normal distribution
    (i.e. mad( N(0, sigma^2) ) = sigma).
    :param axis: For multidimensional arrays, which axis to calculate over
    :param keepdims: If True, axis is kept as dimension of length 1

    :returns: a tuple containing the median and MAD of the data
    """
    if factor is None:
        factor = MED_NORM_FACTOR
    dmed = np.median(data, axis=axis, keepdims=True)
    dmad = factor * np.median(abs(data - dmed), axis=axis, keepdims=True)
    if axis is None:
        dmed = dmed.flatten()[0]
        dmad = dmad.flatten()[0]
    elif not keepdims:
        dmed = dmed.squeeze(axis)
        dmad = dmad.squeeze(axis)
    return dmed, dmad


#####################
# File-type Parsers #
#####################

def str_strand_to_int(strand_str):
    """ Convert string stand representation to integer +/-1 as used in
    minimap2/mappy
    """
    if strand_str == '+':
        return 1
    elif strand_str == '-':
        return -1
    return None


def int_strand_to_str(strand_str):
    """ Convert string stand representation to integer +/-1 as used in
    minimap2/mappy
    """
    if strand_str == 1:
        return '+'
    elif strand_str == -1:
        return '-'
    return '.'


def parse_beds(bed_fns, ignore_strand=False, show_prog_bar=True):
    """ Parse bed files.

    Arguments:
        bed_fns: Iterable containing bed paths
        ignore_strand: Set strand values to None

    Returns:
        Dictionary with keys (chromosome, strand) and values with set of
        0-based coordiantes.
    """
    sites = defaultdict(set)
    for bed_fn in bed_fns:
        with open(bed_fn) as bed_fp:
            bed_iter = (tqdm(bed_fp, desc=bed_fn, smoothing=0)
                        if show_prog_bar else bed_fp)
            for line in bed_iter:
                chrm, start, _, _, _, strand = line.split()[:6]
                start = int(start)
                store_strand = None if ignore_strand else \
                    int_strand_to_str(strand)
                sites[(chrm, store_strand)].add(start)

    # convert to standard dict
    sites = dict(sites)

    return sites


def parse_bed_methyls(bed_fns, strand_offset=None, show_prog_bar=True):
    """ Parse bedmethyl files and return two dictionaries containing
    total and methylated coverage. Both dictionaries have top level keys
    (chromosome, strand) and second level keys with 0-based position.

    Arguments:
        bed_fns: Iterable containing bed methyl paths
        strand_offset: Set to aggregate negative strand along with positive
            strand values. Positive indicates negative strand sites have higher
            coordinate values.
    """
    cov = defaultdict(lambda: defaultdict(int))
    meth_cov = defaultdict(lambda: defaultdict(int))
    for bed_fn in bed_fns:
        with open(bed_fn) as bed_fp:
            bed_iter = (tqdm(bed_fp, desc=bed_fn, smoothing=0)
                        if show_prog_bar else bed_fp)
            for line in bed_iter:
                (chrm, start, _, _, _, strand, _, _, _, num_reads,
                 pct_meth) = line.split()
                start = int(start)
                # convert to 1/-1 strand storage (matching mappy)
                store_strand = int_strand_to_str(strand)
                if strand_offset is not None:
                    # store both strand counts under None
                    store_strand = None
                    # apply offset to reverse strand positions
                    if strand == '-':
                        start -= strand_offset
                num_reads = int(num_reads)
                if num_reads <= 0:
                    continue
                meth_reads = int((float(pct_meth) / 100.0) * num_reads)
                cov[(chrm, store_strand)][start] += num_reads
                meth_cov[(chrm, store_strand)][start] += meth_reads

    # convert to standard dicts
    cov = dict((k, dict(v)) for k, v in cov.items())
    meth_cov = dict((k, dict(v)) for k, v in meth_cov.items())

    return cov, meth_cov


def text_to_bool(val):
    """ Convert text value to boolean.
    """
    lower_val = str(val).lower()
    if lower_val in TRUE_TEXT_VALUES:
        return True
    elif lower_val in FALSE_TEXT_VALUES:
        return False
    raise MegaError('Invalid boolean string encountered: "{}".'.format(val))


def parse_ground_truth_file(gt_data_fn, include_strand=True):
    """ Parse a ground truth data file. CSV with chrm, pos, is_mod values.
    As generated by create_mod_ground_truth.py.

    Args:
        gt_data_fn (str): Filename to be read and parsed.
        include_strand (boolean): Include strand values in parsed position
            values.

    Returns:
        Two sets of position values. First set is ground truth `True` sites and
        second are `False` sites. Values are (chrm, strand, pos) if
        include_strand is True, else values are (chrm, pos). Strand is encoded
        as +/-1 to match minimap2/mappy strands.
    """
    gt_mod_pos = set()
    gt_can_pos = set()
    with open(gt_data_fn) as fp:
        for line in fp:
            chrm, strand, pos, is_mod = line.strip().split(',')
            pos_key = (chrm, str_strand_to_int(strand), int(pos)) \
                if include_strand else (chrm, int(pos))
            if text_to_bool(is_mod):
                gt_mod_pos.add(pos_key)
            else:
                gt_can_pos.add(pos_key)
    return gt_mod_pos, gt_can_pos


if __name__ == '__main__':
    sys.stderr.write('This is a module. See commands with `megalodon -h`')
    sys.exit(1)
