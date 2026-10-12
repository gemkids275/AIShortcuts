import XCTest
@testable import AI_Shortcuts

final class MissingCustomProviderFieldsTests: XCTestCase {

    // MARK: - missingCustomProviderFields

    func testAllFieldsPresentReturnsEmpty() {
        let result = CommandExecutionEngine.missingCustomProviderFields(
            baseURL: "https://api.example.com",
            apiKey: "sk-test",
            model: "gpt-4o"
        )
        XCTAssertTrue(result.isEmpty)
    }

    func testAllFieldsNilReturnsAllThree() {
        let result = CommandExecutionEngine.missingCustomProviderFields(
            baseURL: nil,
            apiKey: nil,
            model: nil
        )
        XCTAssertEqual(result, ["Base URL", "API Key", "Model"])
    }

    func testEmptyStringsAreTreatedAsMissing() {
        let result = CommandExecutionEngine.missingCustomProviderFields(
            baseURL: "",
            apiKey: "",
            model: ""
        )
        XCTAssertEqual(result, ["Base URL", "API Key", "Model"])
    }

    func testWhitespaceOnlyStringsAreTreatedAsMissing() {
        let result = CommandExecutionEngine.missingCustomProviderFields(
            baseURL: "   ",
            apiKey: "\t\n",
            model: "  \t  "
        )
        XCTAssertEqual(result, ["Base URL", "API Key", "Model"])
    }

    func testOnlyBaseURLMissing() {
        let result = CommandExecutionEngine.missingCustomProviderFields(
            baseURL: nil,
            apiKey: "sk-test",
            model: "gpt-4o"
        )
        XCTAssertEqual(result, ["Base URL"])
    }

    func testOnlyApiKeyMissing() {
        let result = CommandExecutionEngine.missingCustomProviderFields(
            baseURL: "https://api.example.com",
            apiKey: nil,
            model: "gpt-4o"
        )
        XCTAssertEqual(result, ["API Key"])
    }

    func testOnlyModelMissing() {
        let result = CommandExecutionEngine.missingCustomProviderFields(
            baseURL: "https://api.example.com",
            apiKey: "sk-test",
            model: nil
        )
        XCTAssertEqual(result, ["Model"])
    }

    // MARK: - customProviderConfigurationErrorIfIncomplete

    func testCompleteConfigReturnsNil() {
        let error = CommandExecutionEngine.customProviderConfigurationErrorIfIncomplete(
            commandName: "Test",
            baseURL: "https://api.example.com",
            apiKey: "sk-test",
            model: "gpt-4o"
        )
        XCTAssertNil(error)
    }

    func testIncompleteConfigReturnsErrorWithCommandName() {
        let error = CommandExecutionEngine.customProviderConfigurationErrorIfIncomplete(
            commandName: "Proofread",
            baseURL: nil,
            apiKey: "sk-test",
            model: "gpt-4o"
        )

        guard case .customProviderConfigurationIncomplete(let name, let fields)? = error else {
            XCTFail("Expected customProviderConfigurationIncomplete error")
            return
        }

        XCTAssertEqual(name, "Proofread")
        XCTAssertEqual(fields, ["Base URL"])
    }

    func testIncompleteConfigMultipleMissingFields() {
        let error = CommandExecutionEngine.customProviderConfigurationErrorIfIncomplete(
            commandName: "Rewrite",
            baseURL: "",
            apiKey: nil,
            model: "gpt-4o"
        )

        XCTAssertEqual(error?.missingCustomProviderFields, ["Base URL", "API Key"])
    }

    func testErrorDescriptionContainsMissingFieldNames() {
        let error = CommandExecutionEngine.customProviderConfigurationErrorIfIncomplete(
            commandName: "Test",
            baseURL: nil,
            apiKey: nil,
            model: nil
        )

        let description = error?.errorDescription ?? ""
        XCTAssertTrue(description.contains("Base URL"))
        XCTAssertTrue(description.contains("API Key"))
        XCTAssertTrue(description.contains("Model"))
        XCTAssertTrue(description.contains("Test"))
    }
}
