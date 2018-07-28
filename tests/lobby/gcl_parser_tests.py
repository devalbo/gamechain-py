import unittest
import gcl_message
import gcl_message_builder
import gcl_parser
from bitcash import PrivateKey


class MsgTestCase(unittest.TestCase):
    def test_lfg_message_build_parse(self):
        # Arrange
        init_conditions = "TICTACTOE;1;X"
        my_key = PrivateKey()

        # Act
        lfg_bytes = gcl_message_builder.create_looking_for_game_message(my_key, init_conditions)
        msg_type, msg = gcl_parser.parse_op_return(lfg_bytes)

        # Assert
        self.assertEqual(gcl_message.MSG_LFG, msg_type)
        self.assertEqual(init_conditions, msg.msg_data)


    def test_wtp_message_build_parse(self):
        # Arrange
        txid_str = '661846ba70aa40862c824d707b62bb4cd1b93d88c01c0bdeb4009112a151a211'
        txid_bytes = bytes.fromhex(txid_str)
        response = "TICTACTOE;1;X"
        my_key = PrivateKey()

        # Act
        wtp_bytes = gcl_message_builder.create_willing_to_play_message(my_key, txid_bytes, response)
        msg_type, msg = gcl_parser.parse_op_return(wtp_bytes)

        # Assert
        self.assertEqual(gcl_message.MSG_WTP, msg_type)
        self.assertEqual(response, msg.msg_data)


    def test_accept_wtp_message_build_parse(self):
        # Arrange
        txid_str = '661846ba70aa40862c824d707b62bb4cd1b93d88c01c0bdeb4009112a151a211'
        txid_bytes = bytes.fromhex(txid_str)
        final_setup_info = "TICTACTOE;1;X"
        my_key = PrivateKey()
        sender_public_key = my_key.public_key

        # Act
        acc_bytes = gcl_message_builder.create_accept_wtp_message(my_key, txid_bytes, final_setup_info)
        msg_type, msg = gcl_parser.parse_op_return(acc_bytes, sender_public_key)

        # Assert
        self.assertEqual(gcl_message.MSG_ACC, msg_type)
        self.assertEqual(final_setup_info, msg.msg_data)


    def test_reject_wtp_message_build_parse(self):
        # Arrange
        txid_str = '661846ba70aa40862c824d707b62bb4cd1b93d88c01c0bdeb4009112a151a211'
        txid_bytes = bytes.fromhex(txid_str)
        rejection_msg = "REJECT-TICTACTOE;1;X"
        my_key = PrivateKey()
        sender_public_key = my_key.public_key

        # Act
        acc_bytes = gcl_message_builder.create_reject_wtp_message(my_key, txid_bytes, rejection_msg)
        msg_type, msg = gcl_parser.parse_op_return(acc_bytes, sender_public_key)

        # Assert
        self.assertEqual(gcl_message.MSG_REJ, msg_type)
        self.assertEqual(rejection_msg, msg.msg_data)


    def test_cancel_lfg_message_build_parse(self):
        # Arrange
        txid_str = '661846ba70aa40862c824d707b62bb4cd1b93d88c01c0bdeb4009112a151a211'
        txid_bytes = bytes.fromhex(txid_str)
        cancel_msg = "CANCEL-TICTACTOE;1;X"
        my_key = PrivateKey()
        sender_public_key = my_key.public_key

        # Act
        acc_bytes = gcl_message_builder.create_cancel_lfg_message(my_key, txid_bytes, cancel_msg)
        msg_type, msg = gcl_parser.parse_op_return(acc_bytes, sender_public_key)

        # Assert
        self.assertEqual(gcl_message.MSG_CAN, msg_type)
        self.assertEqual(cancel_msg, msg.msg_data)

