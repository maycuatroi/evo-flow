from evoflow.Entities.Common import Step


def get_all_common_steps():
    return Step.get_all_common_steps()


def get_all_common_steps_name():
    return [step.name for step in get_all_common_steps()]


if __name__ == "__main__":
    data = get_all_common_steps()
    for key, value in data.items():
        print(f"{key} - {str(value)}")
