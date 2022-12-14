import argparse
import json
import panasoniceolia

from enum import Enum

def print_result(obj, indent = 0):
    for key in obj:
        value = obj[key]

        if isinstance(value, dict):
            print(" "*indent + key)
            print_result(value, indent + 4)
        elif isinstance(value, Enum):
            print(" "*indent + "{0: <{width}}: {1}".format(key, value.name, width=25-indent))
        elif isinstance(value, list):
            print(" "*indent + "{0: <{width}}:".format(key, width=25-indent))
            for elt in value:
                print_result(elt, indent + 4)
                print("")
        else:
            print(" "*indent + "{0: <{width}}: {1}".format(key, value, width=25-indent))

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main():
    """ Start panasoniceolia command line """

    parser = argparse.ArgumentParser(
        description='Read or change status of panasoniceolia Climate devices')

    parser.add_argument(
        'username',
        help='Username for Panasonic Eolia')

    parser.add_argument(
        'password',
        help='Password for Panasoniceolia')

    parser.add_argument(
        '-t', '--token',
        help='File to store token in',
        default='~/.panasoniceolia-token')

    parser.add_argument(
        '-s', '--skipVerify',
        help='Skip Ssl verification if set as True',
        type=str2bool, nargs='?', const=True,
        default=False)

    parser.add_argument(
        '-r', '--raw',
        help='Raw dump of response',
        type=str2bool, nargs='?', const=True,
        default=False)

    commandparser = parser.add_subparsers(
        help='commands',
        dest='command')

    commandparser.add_parser(
        'list',
        help="Get a list of all devices")

    get_parser = commandparser.add_parser(
        'get',
        help="Get status of a device")

    get_parser.add_argument(
        dest='device',
        type=int,
        help='Device number #')

    set_parser = commandparser.add_parser(
        'set',
        help="Set status of a device")

    set_parser.add_argument(
        dest='device',
        type=int,
        help='Device number #'
    )

    set_parser.add_argument(
        '-p', '--power',
        choices=[
            panasoniceolia.constants.Power.On.name,
            panasoniceolia.constants.Power.Off.name],
        help='Power mode')

    set_parser.add_argument(
        '-t', '--temperature',
        type=float,
        help="Temperature")

    set_parser.add_argument(
        '-f', '--fanSpeed',
        choices=[
            panasoniceolia.constants.FanSpeed.Auto.name,
            panasoniceolia.constants.FanSpeed.Low.name,
            panasoniceolia.constants.FanSpeed.LowMid.name,
            panasoniceolia.constants.FanSpeed.Mid.name,
            panasoniceolia.constants.FanSpeed.HighMid.name,
            panasoniceolia.constants.FanSpeed.High.name],
        help='Fan speed')

    set_parser.add_argument(
        '-m', '--mode',
        choices=[
            panasoniceolia.constants.OperationMode.Auto.name,
            panasoniceolia.constants.OperationMode.Cool.name,
            panasoniceolia.constants.OperationMode.Dry.name,
            panasoniceolia.constants.OperationMode.Heat.name,
            panasoniceolia.constants.OperationMode.Fan.name],
        help='Operation mode')

    # set_parser.add_argument(
    #     '-e', '--eco',
    #     choices=[
    #         panasoniceolia.constants.EcoMode.Auto.name,
    #         panasoniceolia.constants.EcoMode.Quiet.name,
    #         panasoniceolia.constants.EcoMode.Powerful.name],
    #     help='Eco mode')

    # set_parser.add_argument(
    #     '--airswingauto',
    #     choices=[
    #         panasoniceolia.constants.AirSwingAutoMode.Disabled.name,
    #         panasoniceolia.constants.AirSwingAutoMode.AirSwingLR.name,
    #         panasoniceolia.constants.AirSwingAutoMode.AirSwingUD.name,
    #         panasoniceolia.constants.AirSwingAutoMode.Both.name],
    #     help='Automation of air swing')

    set_parser.add_argument(
        '-y', '--airSwingVertical',
        choices=[
            panasoniceolia.constants.AirSwingUD.Auto.name,
            panasoniceolia.constants.AirSwingUD.Down.name,
            panasoniceolia.constants.AirSwingUD.DownMid.name,
            panasoniceolia.constants.AirSwingUD.Mid.name,
            panasoniceolia.constants.AirSwingUD.UpMid.name,
            panasoniceolia.constants.AirSwingUD.Up.name],
        help='Vertical position of the air swing')

    set_parser.add_argument(
        '-x', '--airSwingHorizontal',
        choices=[
            panasoniceolia.constants.AirSwingLR.Auto.name,
            panasoniceolia.constants.AirSwingLR.Left.name,
            panasoniceolia.constants.AirSwingLR.LeftMid.name,
            panasoniceolia.constants.AirSwingLR.Mid.name,
            panasoniceolia.constants.AirSwingLR.RightMid.name,
            panasoniceolia.constants.AirSwingLR.Right.name],
        help='Horizontal position of the air swing')

    dump_parser = commandparser.add_parser(
        'dump',
        help="Dump data of a device")

    dump_parser.add_argument(
        dest='device',
        type=int,
        help='Device number 1-x')

    history_parser = commandparser.add_parser(
        'history',
        help="Dump history of a device")

    history_parser.add_argument(
        dest='device',
        type=int,
        help='Device number 1-x')

    history_parser.add_argument(
        dest='mode',
        type=str,
        help='mode (Day, Week, Month, Year)')

    history_parser.add_argument(
        dest='date',
        type=str,
        help='date of day like 20190807')

    args = parser.parse_args()

    session = panasoniceolia.Session(args.username, args.password, args.token, args.raw, args.skipVerify == False)
    session.login()
    try:
        if args.command == 'list':
            print("list of devices and its device id (1-x)")
            for idx, device in enumerate(session.get_devices()):
                if(idx > 0):
                    print('')

                print("device #{}".format(idx + 1))
                print_result(device, 4)

        if args.command == 'get':
            if int(args.device) <= 0 or int(args.device) > len(session.get_devices()):
                raise Exception("device not found, acceptable device id is from {} to {}".format(1, len(session.get_devices())))

            device = session.get_devices()[int(args.device) - 1]
            print("reading from device '{}' ({})".format(device['name'], device['id']))

            print_result( session.get_device(device['id']) )

        if args.command == 'set':
            if int(args.device) <= 0 or int(args.device) > len(session.get_devices()):
                raise Exception("device not found, acceptable device id is from {} to {}".format(1, len(session.get_devices())))

            device = session.get_devices()[int(args.device) - 1]
            print("writing to device '{}' ({})".format(device['name'], device['id']))

            kwargs = {}

            if args.power is not None:
                kwargs['power'] = panasoniceolia.constants.Power[args.power]

            if args.temperature is not None:
                kwargs['temperature'] = args.temperature

            if args.fanSpeed is not None:
                kwargs['fanSpeed'] = panasoniceolia.constants.FanSpeed[args.fanSpeed]

            if args.mode is not None:
                kwargs['mode'] = panasoniceolia.constants.OperationMode[args.mode]

            if args.airSwingHorizontal is not None:
                kwargs['airSwingHorizontal'] = panasoniceolia.constants.AirSwingLR[args.airSwingHorizontal]

            if args.airSwingVertical is not None:
                kwargs['airSwingVertical'] = panasoniceolia.constants.AirSwingUD[args.airSwingVertical]

            session.set_device(device['id'], **kwargs)

        if args.command == 'dump':
            if int(args.device) <= 0 or int(args.device) > len(session.get_devices()):
                raise Exception("device not found, acceptable device id is from {} to {}".format(1, len(session.get_devices())))

            device = session.get_devices()[int(args.device) - 1]

            print_result(session.dump(device['id']))

        # if args.command == 'history':
        #     if int(args.device) <= 0 or int(args.device) > len(session.get_devices()):
        #         raise Exception("device not found, acceptable device id is from {} to {}".format(1, len(session.get_devices())))

        #     device = session.get_devices()[int(args.device) - 1]

        #     print_result(session.history(device['id'], args.mode, args.date))

    except panasoniceolia.ResponseError as ex:
        print(ex.text)


# pylint: disable=C0103
if __name__ == "__main__":
    main()
