import XCTest
@testable import AI_Shortcuts

final class ApplyCharacterDiffTests: XCTestCase {

    func testIdenticalStringsReturnsTrueAndPreservesContent() {
        let attrString = NSMutableAttributedString(string: "Hello world")
        let result = attrString.applyCharacterDiff(from: "Hello world", to: "Hello world")
        XCTAssertTrue(result)
        XCTAssertEqual(attrString.string, "Hello world")
    }

    func testReplacementAtEnd() {
        let attrString = NSMutableAttributedString(string: "Hello world")
        let result = attrString.applyCharacterDiff(from: "Hello world", to: "Hello there")
        XCTAssertTrue(result)
        XCTAssertEqual(attrString.string, "Hello there")
    }

    func testReplacementAtBeginning() {
        let attrString = NSMutableAttributedString(string: "Hello world")
        let result = attrString.applyCharacterDiff(from: "Hello world", to: "Greetings world")
        XCTAssertTrue(result)
        XCTAssertEqual(attrString.string, "Greetings world")
    }

    func testReplacementInMiddle() {
        let attrString = NSMutableAttributedString(string: "Hello beautiful world")
        let result = attrString.applyCharacterDiff(
            from: "Hello beautiful world",
            to: "Hello wonderful world"
        )
        XCTAssertTrue(result)
        XCTAssertEqual(attrString.string, "Hello wonderful world")
    }

    func testCompleteReplacement() {
        let attrString = NSMutableAttributedString(string: "abc")
        let result = attrString.applyCharacterDiff(from: "abc", to: "xyz")
        XCTAssertTrue(result)
        XCTAssertEqual(attrString.string, "xyz")
    }

    func testInsertionOnly() {
        let attrString = NSMutableAttributedString(string: "Hello world")
        let result = attrString.applyCharacterDiff(
            from: "Hello world",
            to: "Hello big world"
        )
        XCTAssertTrue(result)
        XCTAssertEqual(attrString.string, "Hello big world")
    }

    func testDeletionOnly() {
        let attrString = NSMutableAttributedString(string: "Hello big world")
        let result = attrString.applyCharacterDiff(
            from: "Hello big world",
            to: "Hello world"
        )
        XCTAssertTrue(result)
        XCTAssertEqual(attrString.string, "Hello world")
    }

    func testPreconditionFailsWhenReceiverDoesNotMatchSource() {
        let attrString = NSMutableAttributedString(string: "Different content")
        let result = attrString.applyCharacterDiff(from: "Original content", to: "New content")
        XCTAssertFalse(result)
        // The receiver should remain unchanged since precondition failed
        XCTAssertEqual(attrString.string, "Different content")
    }

    func testEmptyToNonEmpty() {
        let attrString = NSMutableAttributedString(string: "")
        let result = attrString.applyCharacterDiff(from: "", to: "New text")
        XCTAssertTrue(result)
        XCTAssertEqual(attrString.string, "New text")
    }

    func testNonEmptyToEmpty() {
        let attrString = NSMutableAttributedString(string: "Old text")
        let result = attrString.applyCharacterDiff(from: "Old text", to: "")
        XCTAssertTrue(result)
        XCTAssertEqual(attrString.string, "")
    }

    func testPreservesAttributesAroundChange() {
        let attrString = NSMutableAttributedString(string: "Hello world")
        let boldRange = NSRange(location: 0, length: 5) // "Hello"
        attrString.addAttribute(.font, value: NSFont.boldSystemFont(ofSize: 14), range: boldRange)

        let result = attrString.applyCharacterDiff(
            from: "Hello world",
            to: "Hello there"
        )
        XCTAssertTrue(result)
        XCTAssertEqual(attrString.string, "Hello there")

        // The bold attribute on "Hello" should be preserved
        var effectiveRange = NSRange()
        let font = attrString.attribute(.font, at: 0, effectiveRange: &effectiveRange) as? NSFont
        XCTAssertNotNil(font)
        // Bold attribute should at least cover the original "Hello" prefix
        XCTAssertGreaterThanOrEqual(effectiveRange.length, 5)
    }

    func testUnicodeCharacters() {
        let attrString = NSMutableAttributedString(string: "Hello 🌍 world")
        let result = attrString.applyCharacterDiff(
            from: "Hello 🌍 world",
            to: "Hello 🌎 world"
        )
        XCTAssertTrue(result)
        XCTAssertEqual(attrString.string, "Hello 🌎 world")
    }

    func testMultibyteCharactersWithAccents() {
        let attrString = NSMutableAttributedString(string: "café latte")
        let result = attrString.applyCharacterDiff(
            from: "café latte",
            to: "café mocha"
        )
        XCTAssertTrue(result)
        XCTAssertEqual(attrString.string, "café mocha")
    }
}
