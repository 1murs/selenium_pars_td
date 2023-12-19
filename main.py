from registration import AccountConnection
from selection_parameters import SelectParameters
from parameters import games, first_service, second_service
from credentials import login, password
import os


class StartChain(SelectParameters):

    def __init__(self, game, first_service, second_service, price_from, price_to, steam_sales=100):
        """
        Initializes the StartChain object.

        Parameters:
        - game (int): The identifier of the selected game.
        - first_service (int): The identifier of the first service.
        - second_service (int): The identifier of the second service.
        - price_from (float): The minimum price for product comparison.
        - price_to (float): The maximum price for product comparison.
        - steam_sales (int): The number of sales for Steam (default is 100).

        Actions:
        - Checks for the presence of a cookie file.
        - If the cookie file is not present, performs login and saves cookies.
        - Calls the constructor of the parent class (SelectParameters) to set parameters.
        """
        # Check for the presence of a cookie file
        if not self.check_cookies_exist:
            self.login_and_save_cookies()
        # Call the constructors of parent classes
        super().__init__(game, first_service, second_service, price_from, price_to, steam_sales)

    @property
    def check_cookies_exist(self) -> bool:
        """
        Checks for the presence of a cookie file.

        Returns:
        - bool: True if the cookie file exists, False otherwise.
        """
        cookies_file_path = 'cookies.pkl'
        return os.path.exists(cookies_file_path)

    @staticmethod
    def login_and_save_cookies():
        """
        Initiates the login process and saves cookies.

        Actions:
        - Creates an instance of the AccountConnection class.
        - Invokes the save_cookies method to perform the login and save cookies.
        """
        create_cookies = AccountConnection(login, password)
        create_cookies.save_cookies()


# run
if __name__ == '__main__':
    game = games[int(input(
        'Select the game: \n1 ==> [ CSGO ] | 2 ==> [ Dota 2 ] | 3 ==> [ Rust ] | 4 ==> [ TF2 ]\nYour choice: '))]
    f_service = first_service[int(input(
        '\nSelect a service for the first: \n1 ==> [ SteamCommunity.com ] | 2 ==> [ BitSkins.com ] | 3 ==> [ TM Market ] | 4 ==> [ DMarket.com ]\nYour choice: '))]
    s_service = second_service[int(input(
        '\nSelect a service for the second: \n1 ==> [ SteamCommunity.com ] | 2 ==> [ BitSkins.com ] | 3 ==> [ TM Market ] | 4 ==> [ DMarket.com ]\nYour choice: '))]
    price_f = float(input('\nPrice from: '))
    price_t = float(input('\nPrice to: '))
    sales_steam = int(input('\nNumber of sales for steam: '))

    runner = StartChain(game, f_service, s_service, price_f, price_t, sales_steam)
    runner.set_cookies()
    runner.browser_action()
    runner.page_parsing()
