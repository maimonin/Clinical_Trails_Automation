import tests_sim


async def test():
    output = await tests_sim.run('jsons/questionnaire_example.json', 'Answers/questionnaire_example_answers1.json',
                                 1, 'female', 20)
