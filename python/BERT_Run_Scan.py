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
        channel         = input("Enter channel [D0, D3]: ")
        inputs = getDefaultInputs(cable_number, channel)
    else:
        # get user inputs
        inputs = getUserInputs()
    # check for inputs
    if not inputs:
        print("ERROR: There are no inputs. Quitting now!")
    # inputs
    tap0_min    = inputs["tap0_min"]
    tap0_max    = inputs["tap0_max"]
    tap0_step   = inputs["tap0_step"]
    signal      = inputs["signal"]
    output_dir  = inputs["output_dir"]
    
    # Press enter to continue...
    input("Press enter to continue... ")
    # run scan
    run(tap0_min, tap0_max, tap0_step, signal, output_dir)

if __name__ == "__main__":
    main()

