# src/calculations.py

import math
from datetime import date

def _calculate_age(birth_date_str):
    """Calcula a idade a partir da string de data de nascimento (YYYY-MM-DD)."""
    birth_date = date.fromisoformat(birth_date_str)
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def _pollock7(sex, age, skinfolds):
    """Calcula a Densidade Corporal usando o protocolo de Pollock de 7 dobras."""
    required_folds = ['chest', 'midaxillary', 'triceps', 'subscapular', 'abdominal', 'suprailiac', 'thigh']
    if not all(k in skinfolds and skinfolds[k] > 0 for k in required_folds):
        return None # Retorna None se alguma dobra necessária estiver faltando

    sum_7_folds = sum(skinfolds[k] for k in required_folds)
    print(sum_7_folds)
    print(sex.lower())
    print(age)

    if sex.lower() == 'masculino':
        body_density = 1.112 - (0.00043499 * sum_7_folds) + (0.00000055 * (sum_7_folds**2)) - (0.00028826 * age)
    elif sex.lower() == 'feminino':
        body_density = 1.097 - (0.00046971 * sum_7_folds) + (0.00000056 * (sum_7_folds**2)) - (0.00012828 * age)
    else:
        return None
    
    print(body_density)
    return (495/body_density)-450

def _pollock3(sex, age, skinfolds):
    """Calcula a Densidade Corporal usando o protocolo de Pollock de 3 dobras."""
    if sex.lower() == 'masculino':
        required_folds = ['chest', 'abdominal', 'thigh']
        if not all(k in skinfolds and skinfolds[k] > 0 for k in required_folds): return None
        sum_3_folds = sum(skinfolds[k] for k in required_folds)
        body_density = 1.10938 - (0.0008267 * sum_3_folds) + (0.0000016 * (sum_3_folds**2)) - (0.0002574 * age)
    elif sex.lower() == 'feminino':
        required_folds = ['triceps', 'suprailiac', 'thigh']
        if not all(k in skinfolds and skinfolds[k] > 0 for k in required_folds): return None
        sum_3_folds = sum(skinfolds[k] for k in required_folds)
        body_density = 1.0994921 - (0.0009929 * sum_3_folds) + (0.0000023 * (sum_3_folds**2)) - (0.0001392 * age)
    else:
        return None
    
    return (495/body_density)-450
    
def _durnin_womersley4(sex, age, skinfolds):
    """Calcula a Densidade Corporal usando o protocolo de Durnin & Womersley de 4 dobras."""
    required_folds = ['biceps', 'triceps', 'subscapular', 'suprailiac']
    if not all(k in skinfolds and skinfolds[k] > 0 for k in required_folds):
        return None

    sum_4_folds = sum(skinfolds[k] for k in required_folds)
    log_sum = math.log10(sum_4_folds)
    
    # Coeficientes C e M variam com idade e sexo
    if sex.lower() == 'masculino':
        if age < 17: c, m = 1.1533, 0.0643
        elif age <= 19: c, m = 1.1620, 0.0630
        elif age <= 29: c, m = 1.1631, 0.0632
        elif age <= 39: c, m = 1.1422, 0.0544
        elif age <= 49: c, m = 1.1620, 0.0700
        else: c, m = 1.1715, 0.0779
    elif sex.lower() == 'feminino':
        if age < 17: c, m = 1.1369, 0.0598
        elif age <= 19: c, m = 1.1549, 0.0678
        elif age <= 29: c, m = 1.1599, 0.0717
        elif age <= 39: c, m = 1.1423, 0.0632
        elif age <= 49: c, m = 1.1333, 0.0612
        else: c, m = 1.1339, 0.0645
    else:
        return None

    body_density = c - (m * log_sum)
    return (495/body_density)-450

def calculate_body_fat(protocol, birth_date_str, sex, skinfolds):
    """
    Função principal que seleciona o protocolo e calcula o percentual de gordura.
    skinfolds: dicionário com as dobras, ex: {'triceps': 10, 'abdominal': 15, ...}
    """
    age = _calculate_age(birth_date_str)
    
    body_fat = None
    
    if protocol == 'Pollock 7 dobras':
        body_fat = _pollock7(sex, age, skinfolds)
        return body_fat
    elif protocol == 'Pollock 3 dobras':
        body_fat = _pollock3(sex, age, skinfolds)
        return body_fat
    elif protocol == 'Durnin & Womersley 4 dobras':
        body_fat = _durnin_womersley4(sex, age, skinfolds)
        return body_fat
    return None # Retorna None se o protocolo for inválido ou faltarem dados