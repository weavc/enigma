import argparse

from .m3.data import rotors, reflectors
from .m3.enigma import enigma
from .m3.settings import settings
from .common import character_arrays
from .web import start

refs = reflectors().names
rots = rotors().names

def run():
    
    parser = setup_parser()
    args = parser.parse_args()

    if args.sub == 'serve':
        start(args.prod)
    else:
        # join plugboard args into string separated by commas
        if args.plugboard is not None:
            args.plugboard = ','.join(args.plugboard)

        s = settings()
        t, errs = s.set_values(**args.__dict__)
        if t == False:
            print('Encountered the following errors:')
            for err in errs:
                print('- ' + err)
            print('')

        v, e = enigma(s).encrypt(' '.join(args.__dict__['input']))
        if e is not None:
            print(e)
        else:
            print('output: ' + v)

def setup_parser():
    parser = argparse.ArgumentParser(
        description='Python M3 Enigma emulator')

    sub = parser.add_subparsers(dest='sub')

    web_parser = sub.add_parser('serve')
    web_parser.add_argument('--prod', action='store_true', dest='prod', default=False)

    cmd_parser = sub.add_parser('cmd')

    # input message
    cmd_parser.add_argument('input', metavar='input', type=str, nargs='+',
                        help='input string for encryption/decryption')

    # select rotors
    cmd_parser.add_argument('-rr', '--right-rotor', metavar='<value>', type=str, action='store',
                        help='right (fast) rotor to be used. accepts: '+','.join(rots), choices=rots,
                        dest='right_rotor')

    cmd_parser.add_argument('-mr', '--middle-rotor', metavar='<value>', type=str, action='store',
                        help='middle rotor to be used. accepts: '+','.join(rots), choices=rots,
                        dest='middle_rotor')

    cmd_parser.add_argument('-lr', '--left-rotor', metavar='<value>', type=str, action='store',
                        help='left (slow) rotor to be used. accepts: '+','.join(rots), choices=rots, dest='left_rotor')

    # select reflector
    cmd_parser.add_argument('-r', '--reflector', metavar='<value>', type=str, action='store',
                        help='reflector to use. accepts: '+','.join(refs), choices=refs, dest='reflector')

    # ring settings
    cmd_parser.add_argument('-rR', '--right-ring', metavar='<value>', type=str, action='store',
                        help='alignment of the right rotor to the inner ring (ring setting). accepts values: A-Z',
                        choices=character_arrays.alphabet, dest='right_ring_setting')

    cmd_parser.add_argument('-mR', '--middle-ring', metavar='<value>', type=str, action='store',
                        help='alignment of the middle rotor to the inner ring (ring setting). accepts values: A-Z',
                        choices=character_arrays.alphabet, dest='middle_ring_setting')

    cmd_parser.add_argument('-lR', '--left-ring', metavar='<value>', type=str, action='store',
                        help='alignment of the left rotor to the inner ring (ring setting). accepts values: A-Z',
                        choices=character_arrays.alphabet, dest='left_ring_setting')

    # rotor settings
    cmd_parser.add_argument('-rp', '--right-position', metavar='<value>', type=str, action='store',
                        help='starting position of the right rotor. accepts values: A-Z', choices=character_arrays.alphabet,
                        dest='right_rotor_setting')

    cmd_parser.add_argument('-mp', '--middle-position', metavar='<value>', type=str, action='store',
                        help='starting position of the middle rotor. accepts values: A-Z', choices=character_arrays.alphabet,
                        dest='middle_rotor_setting')

    cmd_parser.add_argument('-lp', '--left-position', metavar='<value>', type=str, action='store',
                        help='starting position of the left rotor. accepts values: A-Z', choices=character_arrays.alphabet,
                        dest='left_rotor_setting')

    # plugboard
    cmd_parser.add_argument('-p', '--plugboard', type=str, action='store', metavar='PL',
                        help='Plugboard character sets, Characters can only be supplied once. Should be sets of 2 characters, seperated with spaces: XY VB AS ...',
                        dest='plugboard',  nargs='+')

    return parser