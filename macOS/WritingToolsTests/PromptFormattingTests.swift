import XCTest
@testable import AI_Shortcuts

final class PromptFormattingTests: XCTestCase {
    func testEffectivePreserveFormattingUsesLegacyBoolean() {
        let command = CommandModel(
            name: "Proofread",
            prompt: "plain prompt",
            icon: "pencil",
            preserveFormatting: true
        )

        XCTAssertTrue(command.effectivePreserveFormatting)
    }

    func testEffectivePreserveFormattingReadsStructuredRule() {
        let command = CommandModel(
            name: "Proofread",
            prompt: """
            {
              "role": "assistant",
              "task": "proofread",
              "rules": {
                "output": "only corrected text",
                "preserve": {
                  "language": "input"
                },
                "preserve_formatting": true
              }
            }
            """,
            icon: "pencil",
            preserveFormatting: false
        )

        XCTAssertTrue(command.effectivePreserveFormatting)
    }

    func testEffectivePreserveFormattingDefaultsToFalseForUnstructuredPrompt() {
        let command = CommandModel(
            name: "Rewrite",
            prompt: "rewrite this",
            icon: "pencil",
            preserveFormatting: false
        )

        XCTAssertFalse(command.effectivePreserveFormatting)
    }
}
