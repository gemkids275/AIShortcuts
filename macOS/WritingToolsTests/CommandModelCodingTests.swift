import XCTest
@testable import AI_Shortcuts

final class CommandModelCodingTests: XCTestCase {

    // MARK: - Round-trip tests

    func testMinimalCommandRoundTrip() throws {
        let original = CommandModel(
            name: "Test",
            prompt: "Do something",
            icon: "pencil"
        )

        let data = try JSONEncoder().encode(original)
        let decoded = try JSONDecoder().decode(CommandModel.self, from: data)

        XCTAssertEqual(decoded.id, original.id)
        XCTAssertEqual(decoded.name, original.name)
        XCTAssertEqual(decoded.prompt, original.prompt)
        XCTAssertEqual(decoded.icon, original.icon)
        XCTAssertFalse(decoded.useResponseWindow)
        XCTAssertFalse(decoded.isBuiltIn)
        XCTAssertFalse(decoded.hasShortcut)
        XCTAssertFalse(decoded.preserveFormatting)
        XCTAssertNil(decoded.providerOverride)
        XCTAssertNil(decoded.modelOverride)
        XCTAssertNil(decoded.customProviderBaseURL)
        XCTAssertNil(decoded.customProviderModel)
    }

    func testFullyPopulatedCommandRoundTrip() throws {
        let id = UUID()
        let original = CommandModel(
            id: id,
            name: "Full Command",
            prompt: "Do everything",
            icon: "star",
            useResponseWindow: true,
            isBuiltIn: true,
            hasShortcut: true,
            preserveFormatting: true,
            providerOverride: "openai",
            modelOverride: "gpt-4o",
            customProviderBaseURL: "https://api.example.com",
            customProviderModel: "custom-model"
        )

        let data = try JSONEncoder().encode(original)
        let decoded = try JSONDecoder().decode(CommandModel.self, from: data)

        XCTAssertEqual(decoded.id, id)
        XCTAssertEqual(decoded.name, "Full Command")
        XCTAssertEqual(decoded.prompt, "Do everything")
        XCTAssertEqual(decoded.icon, "star")
        XCTAssertTrue(decoded.useResponseWindow)
        XCTAssertTrue(decoded.isBuiltIn)
        XCTAssertTrue(decoded.hasShortcut)
        XCTAssertTrue(decoded.preserveFormatting)
        XCTAssertEqual(decoded.providerOverride, "openai")
        XCTAssertEqual(decoded.modelOverride, "gpt-4o")
        XCTAssertEqual(decoded.customProviderBaseURL, "https://api.example.com")
        XCTAssertEqual(decoded.customProviderModel, "custom-model")
    }

    func testArrayRoundTrip() throws {
        let commands = [
            CommandModel(name: "A", prompt: "a", icon: "a.circle"),
            CommandModel(name: "B", prompt: "b", icon: "b.circle", useResponseWindow: true),
        ]

        let data = try JSONEncoder().encode(commands)
        let decoded = try JSONDecoder().decode([CommandModel].self, from: data)

        XCTAssertEqual(decoded.count, 2)
        XCTAssertEqual(decoded[0].name, "A")
        XCTAssertEqual(decoded[1].name, "B")
        XCTAssertTrue(decoded[1].useResponseWindow)
    }

    // MARK: - Encoding (booleans are always written for export transparency)

    func testFalseBoolsAreEncodedExplicitly() throws {
        let command = CommandModel(
            name: "Compact",
            prompt: "test",
            icon: "pencil"
        )

        let data = try JSONEncoder().encode(command)
        let json = try JSONSerialization.jsonObject(with: data) as? [String: Any]

        XCTAssertEqual(json?["useResponseWindow"] as? Bool, false)
        XCTAssertEqual(json?["isBuiltIn"] as? Bool, false)
        XCTAssertEqual(json?["hasShortcut"] as? Bool, false)
        XCTAssertEqual(json?["preserveFormatting"] as? Bool, false)
        // Nil optionals should also be omitted
        XCTAssertNil(json?["providerOverride"])
        XCTAssertNil(json?["modelOverride"])
        XCTAssertNil(json?["customProviderBaseURL"])
        XCTAssertNil(json?["customProviderModel"])
    }

    func testTrueBoolsArePresent() throws {
        let command = CommandModel(
            name: "Full",
            prompt: "test",
            icon: "pencil",
            useResponseWindow: true,
            isBuiltIn: true,
            hasShortcut: true,
            preserveFormatting: true
        )

        let data = try JSONEncoder().encode(command)
        let json = try JSONSerialization.jsonObject(with: data) as? [String: Any]

        XCTAssertEqual(json?["useResponseWindow"] as? Bool, true)
        XCTAssertEqual(json?["isBuiltIn"] as? Bool, true)
        XCTAssertEqual(json?["hasShortcut"] as? Bool, true)
        XCTAssertEqual(json?["preserveFormatting"] as? Bool, true)
    }

    // MARK: - Legacy data compatibility

    func testLegacyApiKeyFieldIsIgnoredDuringDecoding() throws {
        // Simulate JSON from an older version that included customProviderApiKey
        let legacyJSON: [String: Any] = [
            "id": UUID().uuidString,
            "name": "Legacy",
            "prompt": "test",
            "icon": "pencil",
            "customProviderApiKey": "sk-secret-key",
        ]

        let data = try JSONSerialization.data(withJSONObject: legacyJSON)
        // Should decode without error — the legacy key is silently consumed
        let decoded = try JSONDecoder().decode(CommandModel.self, from: data)
        XCTAssertEqual(decoded.name, "Legacy")
    }

    func testMissingOptionalBoolsDefaultToFalse() throws {
        // Minimal JSON with only required fields
        let minimalJSON: [String: Any] = [
            "id": UUID().uuidString,
            "name": "Minimal",
            "prompt": "test",
            "icon": "pencil",
        ]

        let data = try JSONSerialization.data(withJSONObject: minimalJSON)
        let decoded = try JSONDecoder().decode(CommandModel.self, from: data)

        XCTAssertFalse(decoded.useResponseWindow)
        XCTAssertFalse(decoded.isBuiltIn)
        XCTAssertFalse(decoded.hasShortcut)
        XCTAssertFalse(decoded.preserveFormatting)
    }

    // MARK: - Built-in IDs are stable

    func testBuiltInIDsAreStable() {
        XCTAssertEqual(CommandModel.BuiltInID.proofread.uuidString, "00000000-0001-0000-0000-000000000001")
        XCTAssertEqual(CommandModel.BuiltInID.rewrite.uuidString, "00000000-0001-0000-0000-000000000002")
        XCTAssertEqual(CommandModel.BuiltInID.friendly.uuidString, "00000000-0001-0000-0000-000000000003")
        XCTAssertEqual(CommandModel.BuiltInID.professional.uuidString, "00000000-0001-0000-0000-000000000004")
        XCTAssertEqual(CommandModel.BuiltInID.concise.uuidString, "00000000-0001-0000-0000-000000000005")
        XCTAssertEqual(CommandModel.BuiltInID.summary.uuidString, "00000000-0001-0000-0000-000000000006")
        XCTAssertEqual(CommandModel.BuiltInID.keyPoints.uuidString, "00000000-0001-0000-0000-000000000007")
        XCTAssertEqual(CommandModel.BuiltInID.table.uuidString, "00000000-0001-0000-0000-000000000008")
    }

    func testDefaultCommandsCountAndAllBuiltIn() {
        let defaults = CommandModel.defaultCommands
        XCTAssertEqual(defaults.count, 8)
        XCTAssertTrue(defaults.allSatisfy(\.isBuiltIn))
    }

    // MARK: - Equatable

    func testEqualityByAllFields() {
        let id = UUID()
        let a = CommandModel(id: id, name: "A", prompt: "p", icon: "i")
        let b = CommandModel(id: id, name: "A", prompt: "p", icon: "i")
        XCTAssertEqual(a, b)
    }

    func testInequalityWhenNameDiffers() {
        let id = UUID()
        let a = CommandModel(id: id, name: "A", prompt: "p", icon: "i")
        let b = CommandModel(id: id, name: "B", prompt: "p", icon: "i")
        XCTAssertNotEqual(a, b)
    }

    // MARK: - Custom provider key survives persistence round trip

    func testCustomProviderKeyIsNotOverwrittenByExportPlaceholder() throws {
        let id = UUID()
        defer { KeychainManager.shared.deleteCustomProviderApiKeySync(for: id) }
        let command = CommandModel(
            id: id,
            name: "Custom",
            prompt: "p",
            icon: "pencil",
            providerOverride: "custom",
            customProviderBaseURL: "https://example.test",
            customProviderModel: "m"
        )
        KeychainManager.shared.saveCustomProviderApiKeySync("real-secret", for: id)

        let data = try JSONEncoder().encode([command])
        _ = try JSONDecoder().decode([CommandModel].self, from: data)

        XCTAssertEqual(KeychainManager.shared.retrieveCustomProviderApiKeySync(for: id), "real-secret")
    }

    func testPlaceholderWithSurroundingWhitespaceIsAlsoIgnored() throws {
        let id = UUID()
        defer { KeychainManager.shared.deleteCustomProviderApiKeySync(for: id) }
        KeychainManager.shared.saveCustomProviderApiKeySync("real-secret", for: id)
        let json = """
        [{"id":"\(id.uuidString)","name":"L","prompt":"p","icon":"pencil",
          "providerOverride":"custom","customProviderApiKey":"  YOUR_API_KEY_HERE  "}]
        """
        _ = try JSONDecoder().decode([CommandModel].self, from: Data(json.utf8))

        XCTAssertEqual(KeychainManager.shared.retrieveCustomProviderApiKeySync(for: id), "real-secret")
    }

    func testRealLegacyKeyInJSONIsStillMigrated() throws {
        let id = UUID()
        defer { KeychainManager.shared.deleteCustomProviderApiKeySync(for: id) }
        let json = """
        [{"id":"\(id.uuidString)","name":"L","prompt":"p","icon":"pencil",
          "providerOverride":"custom","customProviderApiKey":"legacy-key"}]
        """
        _ = try JSONDecoder().decode([CommandModel].self, from: Data(json.utf8))

        XCTAssertEqual(KeychainManager.shared.retrieveCustomProviderApiKeySync(for: id), "legacy-key")
    }

    // MARK: - Shared command gallery

    /// Every file in the repo's commands/ folder is offered for download on the website,
    /// so each one must decode as an export bundle exactly the way the importer does.
    func testGalleryCommandFilesDecodeAsExportBundles() throws {
        let repoRoot = URL(fileURLWithPath: #filePath)
            .deletingLastPathComponent().deletingLastPathComponent().deletingLastPathComponent()
        let folder = repoRoot.appendingPathComponent("commands")
        let files = try FileManager.default.contentsOfDirectory(at: folder, includingPropertiesForKeys: nil)
            .filter { $0.pathExtension == "json" }
        XCTAssertFalse(files.isEmpty)

        for file in files {
            let bundle = try JSONDecoder().decode(CommandExportData.self, from: Data(contentsOf: file))
            XCTAssertEqual(bundle.appIdentifier, "AIShortcuts", file.lastPathComponent)
            XCTAssertEqual(bundle.commands.count, 1, file.lastPathComponent)
            let command = try XCTUnwrap(bundle.commands.first)
            XCTAssertFalse(command.name.isEmpty, file.lastPathComponent)
            XCTAssertFalse(command.isBuiltIn, file.lastPathComponent)
            XCTAssertNil(command.providerOverride, file.lastPathComponent)
        }
    }
}

@MainActor
final class CommandImportPlanTests: XCTestCase {

    private func bundle(_ commands: [CommandModel]) -> CommandExportData {
        CommandExportData(commands: commands)
    }

    func testGalleryURLFollowsTheAppLanguage() {
        XCTAssertEqual(CommandManager.galleryURL(language: "vi").absoluteString, "https://aishortcuts.github.io/vi/commands/")
        XCTAssertEqual(CommandManager.galleryURL(language: "vi-VN").absoluteString, "https://aishortcuts.github.io/vi/commands/")
        XCTAssertEqual(CommandManager.galleryURL(language: "de").absoluteString, "https://aishortcuts.github.io/commands/")
        XCTAssertEqual(CommandManager.galleryURL(language: "en").absoluteString, "https://aishortcuts.github.io/commands/")
    }

    func testAllCommandsOfABundleAreImported() {
        let a = CommandModel(name: "A", prompt: "Do A", icon: "pencil")
        let b = CommandModel(name: "B", prompt: "Do B", icon: "pencil")

        let result = CommandManager.commandsToImport(from: bundle([a, b]), existing: [])

        XCTAssertEqual(result.map(\.id), [a.id, b.id])
    }

    func testExistingIdBecomesAnIndependentCopy() {
        let a = CommandModel(name: "A", prompt: "Do A", icon: "pencil", hasShortcut: true)

        let result = CommandManager.commandsToImport(from: bundle([a]), existing: [a])

        XCTAssertEqual(result.count, 1)
        XCTAssertNotEqual(result[0].id, a.id)
        XCTAssertEqual(result[0].name, "A (Imported)")
        XCTAssertEqual(result[0].prompt, "Do A")
        XCTAssertFalse(result[0].hasShortcut)
        XCTAssertFalse(result[0].isBuiltIn)
    }

    func testExistingBuiltInIsSkipped() {
        let builtIn = CommandModel(name: "Proofread", prompt: "p", icon: "pencil", isBuiltIn: true)
        let other = CommandModel(name: "B", prompt: "Do B", icon: "pencil")

        let result = CommandManager.commandsToImport(from: bundle([builtIn, other]), existing: [builtIn])

        XCTAssertEqual(result.map(\.id), [other.id])
    }

    func testDuplicateIdsInsideOneBundleAreNotAddedTwice() {
        let a = CommandModel(name: "A", prompt: "Do A", icon: "pencil")

        let result = CommandManager.commandsToImport(from: bundle([a, a]), existing: [])

        XCTAssertEqual(result.count, 2)
        XCTAssertEqual(Set(result.map(\.id)).count, 2)
    }
}
