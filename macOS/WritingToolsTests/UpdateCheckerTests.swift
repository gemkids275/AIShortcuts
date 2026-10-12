import XCTest
@testable import AI_Shortcuts

final class UpdateCheckerTests: XCTestCase {
    func testSemanticVersionComparison() {
        XCTAssertEqual(UpdateChecker.isUpdateAvailable(current: "6.0", latest: "6.1"), true)
        XCTAssertEqual(UpdateChecker.isUpdateAvailable(current: "6.1", latest: "6.1.1"), true)
        XCTAssertEqual(UpdateChecker.isUpdateAvailable(current: "6.1.1", latest: "6.1"), false)
        XCTAssertEqual(UpdateChecker.isUpdateAvailable(current: "6.1", latest: "6.1.0"), false)
    }

    func testInvalidVersionReturnsNil() {
        XCTAssertNil(UpdateChecker.isUpdateAvailable(current: "abc", latest: "6.1"))
    }
}
