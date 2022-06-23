# hvac_cli.py

'''
A command line integration of the hvac controller for use on the command line
'''

def get_arg( parser_args, attr ):
    arg = getattr( parser_args, attr )
    if type(arg) == list:
        return arg[0]
    return arg

if __name__ == "__main__":
    import argparse
    from core.hvac_controller import HVAC_Controller

    description = "Used to controll hvac system via the command line"
    parser = argparse.ArgumentParser( description=description )

    # add parser arguments
    parser.add_argument(
        '-t','--temperature',
        dest='temperature',
        nargs=1,
        type=str,
        help="Temp to set to (in deg. F)",
        default='74'
    )
    parser.add_argument(
        '-m','--mode',
        dest='mode',
        nargs=1,
        type=str,
        help="Mode to set to",
        default="off"
    )
    parser.add_argument(
        '-f','--fan',
        dest='fan_speed',
        nargs=1,
        type=str,
        help="Fan speed to set to",
        default="auto"
    )

    # extract args
    args = parser.parse_args()

    temp = get_arg( args, 'temperature' )
    mode = get_arg( args, 'mode' )
    fan  = get_arg( args, 'fan_speed' )

    allowed_modes = ['off','fan','cool','dry','heat']
    allowed_fan_speeds = ['auto','low','high']
    controller = HVAC_Controller()

    # do some error correction
    if not temp and not mode:
        print("No temp or mode given, turning off...")
    temp = int(temp)
    if temp < 64 or temp > 78:
        print("Temp out of allowed range (64-78), exiting")
        exit()
    if mode not in allowed_modes:
        print( f"Mode not in allowed modes: {mode} not in {str(allowed_modes)}" )
        exit()
    if fan not in allowed_fan_speeds:
        print( f"Mode not in allowed modes: {fan} not in {str(allowed_fan_speeds)}" )
        exit()

    # send the command to the hvac controller
    controller.send( mode, temp=temp, fan=fan )
    print( f"Sent command of mode: {mode}, temp: {temp}, fan:{fan}" )