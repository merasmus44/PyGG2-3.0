#a series of imports and other stuff that will fail if they don't work
from colorama import Fore
try:
    import mask_extension._mask
except Exception as e:
    print(Fore.RED + "Failed to import mask extension: \n" + str(e) + Fore.RESET)
else:
    print(Fore.GREEN + "Sucessfully imported the mask extension" + Fore.RESET)

