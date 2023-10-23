This software is unofficial and is not related in any way to Lidl or Grocy. It is using [lidl-plus](https://github.com/Andre0512/lidl-plus) requests and can stop working at anytime!

# LidGroSyncer
Easily integrate your Lidl receipts into Grocy

This script will:
- Run through all your receipts and process the starred ones
- Check each item's barcode in Grocy:
    - If the product exists in Grocy it will purchase the given quantity of the product
    - If the product doesn't exist it will create the product in Grocy and add the barcode for it.

## Usage
1. Install requirements: 
    ```
    pip install -r requirements.txt
    ```

1. Fill the settings in `settings_example.py` and rename it to `settings.py`.
More info on obtaining Lidl-Plus refresh token: https://github.com/Andre0512/lidl-plus#commandline-tool.
To get the IDs from Grocy, you can go to `Settings` -> `REST API browser` and query the `GET /objects/{entity}` with `locations` or `quantity_units` selected as entity.

1. Open Lidl-Plus app, find the digital receipts that you want processed and star them. (Make sure they are on the "Starred" tab.)

1. Run `lidgrosyncer.py`

