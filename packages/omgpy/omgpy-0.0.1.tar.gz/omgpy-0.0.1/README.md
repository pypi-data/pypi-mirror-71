# omg-py

Python helper for implementing the Onion Mirror Guidelines (OMG)

The Onion Mirror Guidelines are a set of rules enforced by the operator of [DarkDotFail](https://dark.fail) - a dark net directory of confirmed and official Tor .onions - to help
improve the reliability of the information displayed on the website. 

Practically, implementing the OMG shows a commitment to user safety by proving ownership of PGP keys on a regular basis.


## Reference Specification 

https://dark.fail/spec/omg.txt


## Installation

This will install the `omgpy` package globally with `pip`

    git clone https://code.samourai.io/walletguy/omg-py.git
    cd omg-py
    pip3 install .

## Usage

Import OMG

    from omgpy import OMG


Start OMG with the email address of the PGP key you want to sign with. This key must exist already and be correctly loaded in `gpg`. You can also use a key ID instead of an email address.


    omg = OMG("email@example.com")

Define a `template_path`. If this directory exists then you must manually populate it with templates of the files that will be signed. If this directory doesn't exist currently, it will be created automatically in the next step and the default template files will be copied. 

You can always add new template files to the Template directory, you are not limited by the default set.

    omg.template_path = "/Desktop/omg/templates"


You can copy the default set of files that need to be signed in order to comply with the OMG by calling `create_template_files` after setting the `template_path`. This only needs to be done once (and it is optional - if you do not do this, you will need to manually create the template files and place them in your `template_path` directory.)

    omg.create_template_files()


You can optionally declare where you would like the output saved. If this is not set the default location of the files will be in the current working directory where the script is called from.

    omg.public_path = "/Desktop/omg/public"


You are ready to sign.

    omg.sign()

When the files are signed, the output will be saved in a directory called `public`. In this directory will be two additional directories: `signed` and `unsigned`. The `unsigned` directory will contain the raw `.txt` file of what is to be signed and the `signed` directory will contain the corresponding clearsigned `.txt.asc` file.