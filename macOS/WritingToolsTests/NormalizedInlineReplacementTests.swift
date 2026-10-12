import XCTest
@testable import AI_Shortcuts

final class NormalizedInlineReplacementTests: XCTestCase {

    func testOutputReturnedUnchangedWhenOriginalHasNoTrailingNewline() {
        let result = CommandExecutionEngine.normalizedInlineReplacement(
            "Hello world",
            originalSelectedText: "Original text"
        )
        XCTAssertEqual(result, "Hello world")
    }

    func testNewlineAppendedWhenOriginalEndsWithNewlineButOutputDoesNot() {
        let result = CommandExecutionEngine.normalizedInlineReplacement(
            "Hello world",
            originalSelectedText: "Original text\n"
        )
        XCTAssertEqual(result, "Hello world\n")
    }

    func testOutputReturnedUnchangedWhenBothHaveTrailingNewline() {
        let result = CommandExecutionEngine.normalizedInlineReplacement(
            "Hello world\n",
            originalSelectedText: "Original text\n"
        )
        XCTAssertEqual(result, "Hello world\n")
    }

    func testOutputReturnedUnchangedWhenNeitherHasTrailingNewline() {
        let result = CommandExecutionEngine.normalizedInlineReplacement(
            "Hello",
            originalSelectedText: "World"
        )
        XCTAssertEqual(result, "Hello")
    }

    func testEmptyOutputGetsNewlineWhenOriginalEndsWithNewline() {
        let result = CommandExecutionEngine.normalizedInlineReplacement(
            "",
            originalSelectedText: "Some text\n"
        )
        XCTAssertEqual(result, "\n")
    }

    func testEmptyOriginalReturnsOutputUnchanged() {
        let result = CommandExecutionEngine.normalizedInlineReplacement(
            "Output",
            originalSelectedText: ""
        )
        XCTAssertEqual(result, "Output")
    }

    func testMultipleTrailingNewlinesInOriginalStillAppendsOnlyOne() {
        let result = CommandExecutionEngine.normalizedInlineReplacement(
            "Output",
            originalSelectedText: "Original\n\n\n"
        )
        // hasSuffix("\n") is true, output doesn't end with \n → append one
        XCTAssertEqual(result, "Output\n")
    }

    func testOutputWithNewlineAndOriginalWithoutReturnsOutputUnchanged() {
        let result = CommandExecutionEngine.normalizedInlineReplacement(
            "Output\n",
            originalSelectedText: "Original"
        )
        XCTAssertEqual(result, "Output\n")
    }
}
