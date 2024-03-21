# BERT_Run_Scan.py

from BERT_Scan import run, getDefaultInputs, getUserInputs

def main():
    # yes answers (assume lowercase)
    yes_answers = ["y", "yes", "yep", "yeppers", "yeesh", "yeah", "ya", "yas", "yaas", "yaaas", "ja", "da", "si", "oui", "ouais"]
    # ask to use default inputs
    use_defaults = str(input("Use default inputs? [y/n]: "))
    # convert answer to lowercase
    use_defaults = use_defaults.lower()
    
    # get inputs
    inputs = {}
    if use_defaults in yes_answers:
        # get default inputs
        cable_number    = int(input("Enter cable number: "))
        cable_type      = input("Enter cable type [5K, 5K2]: ")
        channel         = input("Enter channel [D0, D1, D2, D3]: ")
        inputs = getDefaultInputs(cable_number, cable_type, channel)
    else:
        # get user inputs
        inputs = getUserInputs()
    # check for inputs
    if not inputs:
        print("ERROR: There are no inputs. Quitting now!")
    # inputs
    port_card_slot  = inputs["port_card_slot"]
    cable_type      = inputs["cable_type"]
    channel         = inputs["channel"]
    tap0_min        = inputs["tap0_min"]
    tap0_max        = inputs["tap0_max"]
    tap0_step       = inputs["tap0_step"]
    signal          = inputs["signal"]
    output_dir      = inputs["output_dir"]
    
    # Press enter to continue...
    input("Press enter to continue... ")
    # run scan
    run(port_card_slot, cable_type, channel, tap0_min, tap0_max, tap0_step, signal, output_dir)

if __name__ == "__main__":
    main()

