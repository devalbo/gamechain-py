import unittest
from gamechain.lobby import gcl_message, gcl_message_builder, gcl_parser
from gamechain.gc_types import GcPrivateKey
from gamechain.comm import gc_comm


def prepend_op_return_data(msg_bytes):
    op_return_bytes = bytes.fromhex(gc_comm.OP_RETURN_PREFIX) + msg_bytes
    return op_return_bytes


class MsgTestCase(unittest.TestCase):
    def test_lfg_message_build_parse(self):
        # Arrange
        init_conditions = "TICTACTOE;1;X"
        my_key = GcPrivateKey()

        lfg_bytes = gcl_message_builder.create_looking_for_game_message(my_key, init_conditions)
        op_return_bytes = prepend_op_return_data(lfg_bytes)
        lfg_bytes = gc_comm.rx_join_op_returns([op_return_bytes], gcl_message.GCL_LOKAD_PREFIX)

        # Act
        msg_type, msg = gcl_parser.parse_gcl_message(lfg_bytes, None)

        # Assert
        self.assertEqual(gcl_message.MSG_LFG, msg_type)
        self.assertEqual(init_conditions, msg.msg_data)

    def test_wtp_message_build_parse(self):
        # Arrange
        txid_str = '661846ba70aa40862c824d707b62bb4cd1b93d88c01c0bdeb4009112a151a211'
        txid_bytes = bytes.fromhex(txid_str)
        response = "TICTACTOE;1;X"
        my_key = GcPrivateKey()

        wtp_bytes = gcl_message_builder.create_willing_to_play_message(my_key, txid_bytes, response)
        op_return_bytes = prepend_op_return_data(wtp_bytes)
        wtp_bytes = gc_comm.rx_join_op_returns([op_return_bytes], gcl_message.GCL_LOKAD_PREFIX)

        # Act
        msg_type, msg = gcl_parser.parse_gcl_message(wtp_bytes, None)

        # Assert
        self.assertEqual(gcl_message.MSG_WTP, msg_type)
        self.assertEqual(response, msg.msg_data)


    def test_accept_wtp_message_build_parse(self):
        # Arrange
        txid_str = '661846ba70aa40862c824d707b62bb4cd1b93d88c01c0bdeb4009112a151a211'
        txid_bytes = bytes.fromhex(txid_str)
        final_setup_info = "TICTACTOE;1;X"
        my_key = GcPrivateKey()
        sender_public_key = my_key.public_key

        acc_bytes = gcl_message_builder.create_accept_wtp_message(my_key, txid_bytes, final_setup_info)
        op_return_bytes = prepend_op_return_data(acc_bytes)
        acc_bytes = gc_comm.rx_join_op_returns([op_return_bytes], gcl_message.GCL_LOKAD_PREFIX)

        # Act
        msg_type, msg = gcl_parser.parse_gcl_message(acc_bytes, sender_public_key)

        # Assert
        self.assertEqual(gcl_message.MSG_ACC, msg_type)
        self.assertEqual(final_setup_info, msg.msg_data)


    def test_reject_wtp_message_build_parse(self):
        # Arrange
        txid_str = '661846ba70aa40862c824d707b62bb4cd1b93d88c01c0bdeb4009112a151a211'
        txid_bytes = bytes.fromhex(txid_str)
        rejection_msg = "REJECT-TICTACTOE;1;X"
        my_key = GcPrivateKey()
        sender_public_key = my_key.public_key

        rej_bytes = gcl_message_builder.create_reject_wtp_message(my_key, txid_bytes, rejection_msg)
        op_return_bytes = prepend_op_return_data(rej_bytes)
        rej_bytes = gc_comm.rx_join_op_returns([op_return_bytes], gcl_message.GCL_LOKAD_PREFIX)

        # Act
        msg_type, msg = gcl_parser.parse_gcl_message(rej_bytes, sender_public_key)

        # Assert
        self.assertEqual(gcl_message.MSG_REJ, msg_type)
        self.assertEqual(rejection_msg, msg.msg_data)


    def test_cancel_lfg_message_build_parse(self):
        # Arrange
        txid_str = '661846ba70aa40862c824d707b62bb4cd1b93d88c01c0bdeb4009112a151a211'
        txid_bytes = bytes.fromhex(txid_str)
        cancel_msg = "CANCEL-TICTACTOE;1;X"
        my_key = GcPrivateKey()
        sender_public_key = my_key.public_key

        cancel_bytes = gcl_message_builder.create_cancel_lfg_message(my_key, txid_bytes, cancel_msg)
        op_return_bytes = prepend_op_return_data(cancel_bytes)
        cancel_bytes = gc_comm.rx_join_op_returns([op_return_bytes], gcl_message.GCL_LOKAD_PREFIX)

        # Act
        msg_type, msg = gcl_parser.parse_gcl_message(cancel_bytes, sender_public_key)

        # Assert
        self.assertEqual(gcl_message.MSG_CAN, msg_type)
        self.assertEqual(cancel_msg, msg.msg_data)

