from malaya.supervised import huggingface as load_huggingface
from malaya.function import describe_availability
from herpetologist import check_type
import logging

logger = logging.getLogger(__name__)

_huggingface_availability = {
    'mesolitica/finetune-noisy-translation-t5-tiny-bahasa-cased-v2': {
        'Size (MB)': 139,
        'BLEU': 41.625536185056305,
        'SacreBLEU Verbose': '73.4/50.1/35.7/25.7 (BP = 0.971 ratio = 0.972 hyp_len = 21400 ref_len = 22027)',
        'Suggested length': 256,
    },
    'mesolitica/finetune-noisy-translation-t5-small-bahasa-cased-v4': {
        'Size (MB)': 242,
        'BLEU': 41.625536185056305,
        'SacreBLEU Verbose': '73.4/50.1/35.7/25.7 (BP = 0.971 ratio = 0.972 hyp_len = 21400 ref_len = 22027)',
        'Suggested length': 256,
    },
    'mesolitica/finetune-noisy-translation-t5-base-bahasa-cased-v2': {
        'Size (MB)': 892,
        'BLEU': 41.625536185056305,
        'SacreBLEU Verbose': '73.4/50.1/35.7/25.7 (BP = 0.971 ratio = 0.972 hyp_len = 21400 ref_len = 22027)',
        'Suggested length': 256,
    },
}


def available_huggingface():
    """
    List available huggingface models.
    """

    logger.info('tested on noisy twitter google translation, https://huggingface.co/datasets/mesolitica/augmentation-test-set')
    return describe_availability(_huggingface_availability)


def huggingface(
    model: str = 'mesolitica/finetune-noisy-translation-t5-small-bahasa-cased-v4',
    lang: str = 'ms',
    force_check: bool = True,
    **kwargs,
):
    """
    Load HuggingFace model to abstractive text augmentation.

    Parameters
    ----------
    model: str, optional (default='mesolitica/finetune-noisy-translation-t5-small-bahasa-cased-v4')
        Check available models at `malaya.augmentation.abstractive.available_huggingface()`.
    lang: str, optional (default='ms')
        Input language, only accept `ms` or `en`.
    force_check: bool, optional (default=True)
        Force check model one of malaya model.
        Set to False if you have your own huggingface model.

    Returns
    -------
    result: malaya.torch_model.huggingface.Generator
    """
    map_lang = {'en': 'Inggeris', 'ms': 'Melayu'}
    lang = lang.lower()
    if lang not in map_lang:
        raise ValueError('`lang` only accept `en` or `ms`.')

    if model not in _huggingface_availability and force_check:
        raise ValueError(
            'model not supported, please check supported models from `malaya.augmentation.abstractive.available_huggingface()`.'
        )
    return load_huggingface.load_generator(
        model=model,
        initial_text=f'terjemah {map_lang[lang]} ke pasar Melayu: ',
        **kwargs)
