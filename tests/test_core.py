import unittest

import core


class TestCore(unittest.TestCase):
    def test_01_no_duplicate_register(self):
        state = core.new_game()
        self.assertTrue(core.register(state, "S1"))
        self.assertFalse(core.register(state, "S1"))

    def test_02_class_capacity(self):
        state = core.new_game()
        core.enroll(state, "S1")
        core.enroll(state, "S2")
        result = core.enroll(state, "S3")
        self.assertFalse(result)

    def test_03_fee_exact(self):
        state = core.new_game()
        self.assertEqual(core.fee(state, "S1", 3), 2)

    def test_04_cancel_refunds_books(self):
        state = core.new_game()
        state["books"] = 90
        core.cancel(state, "S1")
        self.assertEqual(state["books"], 100)

    def test_05_no_assign_absent_teacher(self):
        state = core.new_game()
        core.register(state, "S1")
        result = core.assign(state, "S1", "T2")
        self.assertFalse(result)

    def test_06_exam_fail_no_credit(self):
        state = core.new_game()
        core.register(state, "S1")
        state["students"]["S1"]["failed"] = True
        before = state["credits"]
        result = core.exam(state, "S1")
        self.assertFalse(result)
        self.assertEqual(state["credits"], before)

    def test_07_absence_once(self):
        state = core.new_game()
        core.register(state, "S1")
        state["students"]["S1"]["credits"] = 10
        core.absence(state, "S1")
        self.assertEqual(state["students"]["S1"]["credits"], 9)

    def test_08_load_preserves_student(self):
        state = core.new_game()
        state["student_id"] = 4
        loaded = core.load_state(core.save_state(state))
        self.assertEqual(loaded["student_id"], 4)


if __name__ == "__main__":
    unittest.main()
