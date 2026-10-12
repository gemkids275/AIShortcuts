import XCTest
@testable import AI_Shortcuts

final class CommandExecutionEngineTests: XCTestCase {
    func testIncompleteCustomProviderReturnsExplicitError() {
        let error = CommandExecutionEngine.customProviderConfigurationErrorIfIncomplete(
            commandName: "Rewrite",
            baseURL: "https://api.example.com/v1",
            apiKey: "",
            model: "gpt-4o-mini"
        )

        guard case .customProviderConfigurationIncomplete(let commandName, let missingFields)? = error else {
            XCTFail("Expected customProviderConfigurationIncomplete error")
            return
        }

        XCTAssertEqual(commandName, "Rewrite")
        XCTAssertEqual(missingFields, ["API Key"])
    }

    func testCompleteCustomProviderConfigurationReturnsNoError() {
        let error = CommandExecutionEngine.customProviderConfigurationErrorIfIncomplete(
            commandName: "Rewrite",
            baseURL: "https://api.example.com/v1",
            apiKey: "sk-test",
            model: "gpt-4o-mini"
        )

        XCTAssertNil(error)
    }
}
