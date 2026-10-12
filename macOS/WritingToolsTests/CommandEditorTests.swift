import XCTest
@testable import AI_Shortcuts

final class CommandEditorTests: XCTestCase {
    func testTrimmedNameForSaveRemovesOuterWhitespace() {
        XCTAssertEqual(CommandEditor.trimmedNameForSave("  Proofread  "), "Proofread")
    }

    func testNormalizedNameCollapsesWhitespaceAndCase() {
        let normalized = CommandEditor.normalizedCommandName("  ProoF\n\t   Read   ")
        XCTAssertEqual(normalized, "proof read")
    }

    func testDuplicateNameDetectionIsWhitespaceAndCaseInsensitive() {
        let currentID = UUID()
        let existing = CommandModel(
            id: UUID(),
            name: "  Proof\nread  ",
            prompt: "prompt",
            icon: "pencil"
        )
        let current = CommandModel(
            id: currentID,
            name: "Current",
            prompt: "prompt",
            icon: "pencil"
        )

        let candidate = CommandEditor.normalizedCommandName("proof   READ")
        XCTAssertTrue(
            CommandEditor.hasDuplicateName(
                normalizedCandidateName: candidate,
                currentCommandID: currentID,
                existingCommands: [existing, current]
            )
        )
    }
}
