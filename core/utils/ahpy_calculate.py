import ahpy

async def result_calculator(target_weights: dict):
    result = []
    local_max = 0
    message = "Результат сравнений:\n"
    for key, value in target_weights.items():
        if value > local_max:
            local_max = value
            result = []
            result.append(key)
        elif value == local_max:
            result.append(key)
        message += f"{key}: {value}\n"
    message += f"<b>Поздравляю тебя!</b> В результате анализа всех твоих предпочтений тебе необходимо выбрать {', '.join(result)}"
    return message
async def calculate_target_weights(data: dict):
    compare = []
    for i in range(len(data["criteria"])):
        name = data["criteria"][i]
        comparisons = data["vuz_comparisons"][data["criteria"][i]]
        compare.append(ahpy.Compare(name, comparisons, precision=3, random_index='saaty'))
    criteria = ahpy.Compare('Criteria', data["criteria_comparisons"], precision=3, random_index='saaty')
    criteria.add_children(compare)
    return criteria.target_weights



