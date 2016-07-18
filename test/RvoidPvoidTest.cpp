#include "FooFixture.hpp"

// The function that the user wants to test with replacing call expressions
// inside.
void RvoidPvoidCaller();
// The used functions inside that the user might replace
void RvoidPvoid();
void RvoidPvoid_2();

void fake_RvoidPvoid(); // user provides
// should be generated by a macro
void fake_RvoidPvoid_aux(int count, void *ret_value, int ret_size, ...) {
    ::ftest::called.insert(reinterpret_cast<char *>(fake_RvoidPvoid_aux));

    EXPECT_EQ(count, 0);
    EXPECT_EQ(ret_value, nullptr);
    EXPECT_EQ(ret_size, 0);

    fake_RvoidPvoid();
}
// User provides
void fake_RvoidPvoid() {
    ::ftest::called.insert(reinterpret_cast<char *>(fake_RvoidPvoid));
}

/// signature: void()
TEST_F(FooFixture, RvoidPvoid) {
    ::fake::subs.insert(
        {address(RvoidPvoid), address(fake_RvoidPvoid_aux)});
    RvoidPvoidCaller();

    EXPECT_EQ(::ftest::called.count(address(RvoidPvoid)), 0);
    EXPECT_EQ(::ftest::called.count(address(fake_RvoidPvoid_aux)), 1);
    EXPECT_EQ(::ftest::called.count(address(fake_RvoidPvoid)), 1);
    EXPECT_EQ(::ftest::called.count(address(RvoidPvoid_2)), 1);
}
