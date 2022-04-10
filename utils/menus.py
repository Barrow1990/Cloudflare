import logging


def single_choice_menu(message=str, options=list):
    logging.info(f"| menus | single_choice_menu | message: {message}, options: {options}")
    for option_id, option in enumerate(options):
        print(f"{option_id+1}: {option}")

    while True:
        menu_choice = input(message)
        if menu_choice.isdigit() and int(menu_choice) <= len(options):
            logging.info(f"| menus | single_choice_menu | menu choice: {options[int(menu_choice)-1]}\n")
            return int(menu_choice)-1


def multi_choice_menu(message=str, options=list):
    logging.info(f"| menus | multi_choice_menu | message: {message}, options: {options}")
    user_options = []
    options.append('All')
    while True:
        for option_id, option in enumerate(options):
            print(f"{option_id+1}: {option}")

        print(f"Selected: {user_options}")

        menu_choice = input(message)
        if menu_choice.isdigit() and int(menu_choice) <= len(options):

            if int(menu_choice)-1 == options.index('All'):
                user_options = options
                user_options.remove('All')
                break
            else:
                user_options.append(options[int(menu_choice)-1])
                options.remove(options[int(menu_choice)-1])

        if not menu_choice:
            break

    logging.info(f"| menus | multi_choice_menu | menu choice: {user_options}\n")
    return user_options
