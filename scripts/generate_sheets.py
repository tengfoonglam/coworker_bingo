from coworker_bingo.bingo_sheet_generator import BingoSheetGenerator


def main() -> None:

    number_participants = 30

    participants = [f"Participant{i+1}" for i in range(number_participants)]

    generic_facts = [f"generic fact {i}" for i in range(100)]

    specific_facts = dict()
    number_participants_with_specific_facts = 20
    for i in range(number_participants_with_specific_facts):
        specific_facts[f"Participant{i+1}"] = [f"Participant{i+1} FACT {j+1}" for j in range(3)]

    config = BingoSheetGenerator.Config(sheet_size=5,
                                        participant=participants[0],
                                        participants=set(participants),
                                        generic_facts=generic_facts,
                                        specific_facts=specific_facts,
                                        specific_fact_indexes=set([0, 4, 6, 8, 12, 16, 18, 20, 24]))

    sheet = BingoSheetGenerator.generate(config=config)

    BingoSheetGenerator.draw_table(sheet=sheet, config=config, export_path=f"generated_sheets/{config.participant}.png")


if __name__ == "__main__":
    main()
