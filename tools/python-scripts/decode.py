from natsort import natsorted

#  function to prepare for decoding
def create_pyramid(encoded_message):
  step = 1
  subsets = []
  while len(encoded_message) != 0:
    if len(encoded_message) >= step:
      subsets.append(encoded_message[0:step])
      encoded_message = encoded_message[step:]
      step += 1
    else:
      return False
      
  return subsets

def decode(message_file):
    # read file data
    message_to_decode = message_file.readlines()

    # sort values so the pyramid is built in the right order
    message_to_decode = natsorted(message_to_decode)

    # build the pyramid
    pyramid = create_pyramid(message_to_decode)

    # check if valid input
    if(pyramid == False):
        return "There seem to be some missing or extra values, unable to decode."

    # prep loop and output variables
    i = 0
    decoded_message = ""

    # iteratively grab end elements of each pyramid level
    for step in pyramid:
        decoded_message = decoded_message + " " + step[i][:-1]
        i = i + 1

    # display decoded message, then close file
    return decoded_message

# open text file
file = open('test_message.txt')

# decode file
print(decode(file))

# close file
file.close()