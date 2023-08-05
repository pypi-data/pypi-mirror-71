import numpy as np
from numpy.linalg import inv
import argparse

'''
This is just for practice purpose. Scipy and numpy
have already provided enough tools.
'''
def x_hat(A, b):
    aTa = A.T.dot(A)
    aTa_inv = inv(aTa)
    return aTa_inv.dot(A.T).dot(b)

def project(A=None, b=None):
    '''
    * is dot product
    p = P*b = a*inv(aT*a)*aT*b
    '''
    aTa = A.T.dot(A)
    aTa_inv = inv(aTa)
    x_bar = aTa_inv.dot(A.T)
    p = A.dot(x_bar).dot(b)
    return p, x_bar

def input_to_mx(i):
    return np.array(eval(i))

def run_cmd(parsed_arg, cmd_name):
    '''
    gather arguments for each sub-commands
    and parse arguments into correct data type
    '''
    cmd = eval(getattr(parsed_arg, cmd_name))
    _, *keys= parsed_arg.__dict__.keys()
    _, *values = parsed_arg.__dict__.values()
    transformed_values = [input_to_mx(each) for each in values if each.strip().startswith('[')]
    a = dict(zip(keys, transformed_values))
    return cmd(**a)

def show(result):
    print(result)

def main():
    arg = argparse.ArgumentParser(description='Calculations in Linear Algebra')
    sub_parsers = arg.add_subparsers(
        title='calculation',
        description='enter the calculation to be done',
        help='calculations',
        dest='command',
        required=True
    )

    ###projection###
    projection_args = sub_parsers.add_parser('project', help='project help')
    projection_args.add_argument('-A', '--A', help='matrix to be projected on. example: [[1,2,3], [1,2,3]] is a 2x3 matrix.')
    projection_args.add_argument('-b', '--b', help='matrix to poject')

    args = arg.parse_args()
    
    result = run_cmd(args, 'command')
    show(result)
    



if __name__ == '__main__':
    # A = np.array([1,0,1,1,1,2]).reshape(3,2)
    # b = np.array([6,0,0])
    # print(x_hat(A, b))
    main()