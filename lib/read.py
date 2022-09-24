"""
Example of reading from a card using the ``mfrc522`` module.
"""
# 3rd party
import board

# this package
import mfrc522


def do_read():
	
	rdr = mfrc522.MFRC522(board.GP2, board.GP3, board.GP4, board.GP0, board.GP1)
	rdr.set_antenna_gain(0x07 << 4)

	print('')
	print("Place card before reader to read from address 0x08")
	print('')

	try:
		while True:

			(stat, tag_type) = rdr.request(rdr.REQIDL)
			print("Request: ", stat, tag_type, rdr.OK, rdr.anticoll())
			
			# dump card info

			if stat == rdr.OK:

				(stat, raw_uid) = rdr.anticoll()

				if stat == rdr.OK:
					print("New card detected")
					print("  - tag type: 0x%02x" % tag_type)
					print("  - uid\t : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
					print('')

					if rdr.select_tag(raw_uid) == rdr.OK:

						key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

						if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
							print("Address 8 data: %s" % rdr.read(8))
							rdr.stop_crypto1()
						else:
							print("Authentication error")
					else:
						print("Failed to select tag")

	except KeyboardInterrupt:
		print("Bye")