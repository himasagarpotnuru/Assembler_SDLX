#
#from math import log
#import numpy as np


# def signed_binary()
def bina_rep_for_neg_num(
    n, size):  #coversion of the signed decimal to signed binary number
  a = bin(n & int("1" * size, 2))[2:]
  return ("{0:0>%a}" % (size)).format(a)


opcodes = {
  'add': 1,
  'sub': 2,
  'mul': 3,
  'or': 4,
  'xor': 5,
  'and': 6,
  'sll': 7,
  'sla': 8,
  'sra': 9,
  'srl': 10,
  'ror': 11,
  'rol': 12,
  'slt': 13,
  'sgt': 14,
  'sle': 15,
  'sge': 16,
  'ugt': 17,
  'ult': 18,
  'uge': 19,
  'ule': 20,
  # till here instruction codes goes in R type triadic
  'addi': 21,
  'subi': 22,
  'ori': 23,
  'andi': 24,
  'xori'
  : 25,
  'slli': 26,
  'srli': 27,
  'srai': 28,
  'slti': 29,
  'sgti': 30,
  'slei': 31,
  'sgei': 32,
  'ugti': 33,
  'ulti': 34,
  'ugei': 35,
  'ulei': 36,
  'lhi': 37,
  'lh': 38,
  'sw': 39,
  'sb': 40,
  'sh': 41,
  # from 21 to 41 instruction code goes in RI type triadic
  'bnez': 42,
  'beqz': 43,
  'jr': 44,
  'jalr': 45,
  # These branch instruction goes in R type dyadic
  'j': 46,
  'jal': 47
  # These jump instruction goes in J type
}

Registers = {
  '$r0': 0,
  '$r1': 1,
  '$r2': 2,
  '$r3': 3,
  '$r4': 4,
  '$r5': 5,
  '$r6': 6,
  '$r7': 7,
  '$r8': 8,
  '$r9': 9,
  '$r10': 10,
  '$r11': 11,
  '$r12': 12,
  '$r13': 13,
  '$r14': 14,
  '$r15': 15,
  '$r16': 16,
  '$r17': 17,
  '$r18': 18,
  '$r19': 19,
  '$r20': 20,
  '$r21': 21,
  '$r22': 22,
  '$r23': 23,
  '$r24': 24,
  '$r25': 25,
  '$r26': 26,
  '$r27': 27,
  '$r28': 28,
  '$r29': 29,
  '$r30': 30,
  '$r31': 31
}  #

start_address = int(input('give the base address:'))

if (start_address % 4 != 0):
  print("invalid base address")

else:

  try:
    file_name = input('give the file name:')

    with open(file_name, 'r') as assembler_code:
      lines = [line.rstrip() for line in assembler_code]
    n = len(lines)
    # n represents the number of lines in assembly code including blank
    address = [start_address]
    #for storing the addresses of the corresponding command
    command = []
    label = {}

    #number of lines in the given text file
    nav = 0
    #navigator which will be helped for avoiding the blank lines
    count = 0
    #for running through all the lines

    while nav < (n):
      lines[nav] = lines[nav].strip()  # removing the unnecessary white spaces
      if (len(lines[nav]) == 0):  #eliminating the blank lines
        nav += 1  #skipping to the next line
        continue

      elif (":" in lines[nav]):
        current_line = lines[nav].split(':')
        address.append(address[count] + 4)  #st
        current_line[1] = current_line[1].strip()
        command.append(current_line[1])
        label_name = current_line[0].strip()
        label[label_name] = address[count]
        # stores the address count of the particular for further access in the future
        nav += 1
        count += 1

      else:  #a valid instruction
        current_line = lines[nav].strip()
        command.append(current_line)  #adding it to the list of instructions
        address.append(address[count] + 4)  #update the address
        count += 1
        nav += 1

    address.pop()

    for i in range(len(
        command)):  #iterate over the particular strings to pass the line to a
      a = command[i]
      a = a.replace(",", " ")  # replaces the old value "," with " " in the
      # particular i in function and split with
      # the white spaces in a

      a = a.split()
      if len(a) == 4:
        k = a[0]
        l = a[1]
        m = a[2]

        try:

          Rd = Registers[l]
          Rd_bina = bin(Rd)[2:].zfill(5)
          #zfill fill add the zeroes at the beginnin of the string untill they are of the specified length
          R1 = Registers[m]
          R1_bina = bin(R1)[2:].zfill(5)
          opcode = opcodes[k]

        except:

          print("invalid command_line format in command line ")
          break
        # attaches the specified number here to the opcode from opcodes dictionary in the beginning
        opcode_bina = bin(opcode)[2:].zfill(6)

        if opcode in range(
            1, 21):  # checks whether opcode belong to Rtype triadic
          n = a[3]  # if yes then, it goes on to
          n = str(n)

          try:
            R2 = Registers[n]

          except:

            print("Error occured Register not found")
            break

          R2_bina = bin(R2)[2:].zfill(5)
          R_type_triadic = '000000' + str(R1_bina) + str(R2_bina) + str(
            Rd_bina) + '00000' + str(opcode_bina)  #R type triadic format
          out = R_type_triadic

        elif opcode in range(
            21, 42):  #checks whether opcode belong to RI_type triadic
          imm = int(a[3])
          imm_bina = bin(imm)[2:].zfill(
            16)  #converts the immediate constant into 16 bits
          RI_type_triadic = str(opcode_bina) + str(R1_bina) + str(
            Rd_bina) + str(imm_bina)
          out = RI_type_triadic

        elif opcode in range(42, 46):

          imm = a[3]
          if imm.isnumeric() == False:
            #for branch type instructions checks whether if there is an label configuration in immediate constant space
            imm = label[
              imm]  #takes the particular address for the label to pass
            imm = int(imm)
            p = address[i]
            p = int(p)
            imm = (imm - p - 4) // 4
          else:

            imm = int(imm)
          if (imm >= 0):
            imm_bina = bin(imm)[2:].zfill(16)  #zfill upto 16 bits
          else:
            imm_bina = bina_rep_for_neg_num(imm, 16)
          R_type_diadic = str(opcode_bina) + str(R1_bina) + '00000' + str(
            imm_bina)
          out = R_type_diadic

      elif (len(a) == 2):

        k = a[0]
        opcode = opcodes[k]

        if opcode in range(46, 48):
          opcode_bina = bin(opcode)[2:].zfill(6)
          signedoffest = a[1]

          if signedoffest.isnumeric() == False:
            signedoffest = label[signedoffest]

            #similarly checks whether if there is an label configuration in immediate constant space
            signedoffest = int(signedoffest)
            p = address[i]
            p = int(p)
            signedoffest = (signedoffest - p - 4) // 4
          else:

            signedoffest = int(signedoffest)
          if (signedoffest >= 0):
            signedoffest_bina = bin(signedoffest)[2:].zfill(
              16)  #zfill upto 16 bits
          else:
            signedoffest_bina = bina_rep_for_neg_num(signedoffest, 26)

          J_type = str(opcode_bina) + str(signedoffest_bina)
          out = J_type
      elif (len(a) == 3):
        k = a[0]
        opcode = opcodes[k]
        l = a[1]
        R1 = Registers[l]
        R1_bina = bin(R1)[2:].zfill(5)
        if opcode in range(21, 42):
          opcode_bina = bin(opcode)[2:].zfill(6)
          imm = a[2]
          imm_bina = bin(imm)[2:].zfill(16)
          RI_type_triadic = str(opcode_bina) + str(R1_bina) + '00000' + str(
            imm_bina)
        elif opcode in range(42, 46):
          opcode_bina = bin(opcode)[2:].zfill(6)
          imm = a[2]
          if imm.isnumeric() == False:
            #for branch type instructions checks whether if there is an label configuration in immediate constant space
            imm = label[
              imm]  #takes the particular address for the label to pass
            imm = int(imm)
            p = address[i]
            p = int(p)
            imm = (imm - p - 4) // 4
          else:
            imm = int(imm)
          if (imm >= 0):
            imm_bina = bin(imm)[2:].zfill(16)  #zfill upto 16 bits
          else:
            imm_bina = bina_rep_for_neg_num(imm, 16)
          #zfill upto 16 bits
          R_type_diadic = str(opcode_bina) + str(R1_bina) + '00000' + str(
            imm_bina)
          out = R_type_diadic
      print(out, end='\n')

  except:

    command_line = input('give the command line:')
    a = command_line.strip()

    a = a.replace(",", " ")  # replaces the old value "," with " " in the
    # particular i in function and split with
    # the white spaces in a

    a = a.split()
    if len(a) == 4:
      k = a[0]
      l = a[1]
      m = a[2]

      try:

        Rd = Registers[l]
        Rd_bina = bin(Rd)[2:].zfill(5)
        #zfill fill add the zeroes at the beginnin of the string untill they are of the specified length
        R1 = Registers[m]
        R1_bina = bin(R1)[2:].zfill(5)
        opcode = opcodes[k]

      except:

        print("invalid command_line format in command line ")

      opcode_bina = bin(opcode)[2:].zfill(6)
      if opcode in range(1,
                         21):  # checks whether opcode belong to Rtype triadic
        n = a[3]  # if yes then, it goes on to
        n = str(n)
        R2 = Registers[n]
        try:
          R2 = Registers[n]

        except:

          print("Error occured Register not found")

        R2_bina = bin(R2)[2:].zfill(5)
        R_type_triadic = '000000' + str(R1_bina) + str(R2_bina) + str(
          Rd_bina) + '00000' + str(opcode_bina)  #R type triadic format
        out = R_type_triadic

      elif opcode in range(21,
                           42):  #checks whether opcode belong to Rtype dyadic
        imm = int(a[3])
        imm_bina = bin(imm)[2:].zfill(
          16)  #converts the immediate constant into 16 bits
        RI_type_triadic = str(opcode_bina) + str(R1_bina) + str(Rd_bina) + str(
          imm_bina)
        out = RI_type_triadic

      elif opcode in range(42, 46):
        imm = a[3]

        if imm.isnumeric() == False:
          #for branch type instructions checks whether if there is an label configuration in immediate constant space
          imm = label[imm]  #takes the particular address for the label to pass
          imm = int(imm)
          p = address[i]
          p = int(p)
          imm = (imm - p - 4) // 4
        else:

          imm = int(imm)
        if (imm >= 0):
          imm_bina = bin(imm)[2:].zfill(16)  #zfill upto 16 bits
        else:
          imm_bina = bina_rep_for_neg_num(imm, 16)
        R_type_diadic = str(opcode_bina) + str(R1_bina) + '00000' + str(
          imm_bina)
        out = R_type_diadic

    elif (len(a) == 2):
      k = a[0]
      opcode = opcodes[k]
      if opcode in range(46, 48):
        opcode_bina = bin(opcode)[2:].zfill(6)
        signedoffest = a[1]

        if signedoffest.isnumeric() == False:
          signedoffest = label[signedoffest]
          #similarly checks whether if there is an label configuration in immediate constant space
          signedoffest = int(signedoffest)
          p = address[i]
          p = int(p)
          signedoffest = (signedoffest - p - 4) // 4
        else:

          signedoffest = int(signedoffest)
        if (signedoffest >= 0):
          signedoffest_bina = bin(signedoffest)[2:].zfill(
            16)  #zfill upto 16 bits
        else:
          signedoffest_bina = bina_rep_for_neg_num(signedoffest, 26)
        J_type = str(opcode_bina) + str(signedoffest_bina)
        out = J_type
    elif (len(a) == 3):
      k = a[0]
      opcode = opcodes[k]
      l = a[1]
      R1 = Registers[l]
      R1_bina = bin(R1)[2:].zfill(5)
      if opcode in range(21, 42):
        opcode_bina = bin(opcode)[2:].zfill(6)
        imm = a[2]
        imm_bina = bin(imm)[2:].zfill(16)
        RI_type_triadic = str(opcode_bina) + str(R1_bina) + '00000' + str(
          imm_bina)
      elif opcode in range(42, 46):
        opcode_bina = bin(opcode)[2:].zfill(6)
        imm = a[2]
        if imm.isnumeric() == False:
          #for branch type instructions checks whether if there is an label configuration in immediate constant space
          imm = label[imm]  #takes the particular address for the label to pass
          imm = int(imm)
          p = address[i]
          p = int(p)
          imm = (imm - p - 4) // 4
        else:

          imm = int(imm)
        if (imm >= 0):
          imm_bina = bin(imm)[2:].zfill(16)  #zfill upto 16 bits
        else:
          imm_bina = bina_rep_for_neg_num(imm, 16)
        R_type_diadic = str(opcode_bina) + str(R1_bina) + '00000' + str(
          imm_bina)
        out = R_type_diadic

    print(out, end='\n')
