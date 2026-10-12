import XCTest
@testable import AI_Shortcuts

final class ImageMIMETypeTests: XCTestCase {

    func testJPEGDetection() {
        let jpegData = Data([0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10])
        XCTAssertEqual(detectImageMIMEType(jpegData), "image/jpeg")
    }

    func testPNGDetection() {
        let pngData = Data([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A])
        XCTAssertEqual(detectImageMIMEType(pngData), "image/png")
    }

    func testGIFDetection() {
        let gifData = Data([0x47, 0x49, 0x46, 0x38, 0x39, 0x61])
        XCTAssertEqual(detectImageMIMEType(gifData), "image/gif")
    }

    func testWebPDetection() {
        // WebP starts with RIFF (0x52 0x49 0x46 0x46)
        let webpData = Data([0x52, 0x49, 0x46, 0x46, 0x00, 0x00])
        XCTAssertEqual(detectImageMIMEType(webpData), "image/webp")
    }

    func testUnrecognizedFormatDefaultsToJPEG() {
        let unknownData = Data([0x00, 0x00, 0x00, 0x00, 0x00])
        XCTAssertEqual(detectImageMIMEType(unknownData), "image/jpeg")
    }

    func testEmptyDataDefaultsToJPEG() {
        XCTAssertEqual(detectImageMIMEType(Data()), "image/jpeg")
    }

    func testShortDataDefaultsToJPEG() {
        // Less than 4 bytes
        let shortData = Data([0x89, 0x50])
        XCTAssertEqual(detectImageMIMEType(shortData), "image/jpeg")
    }

    func testThreeByteDataDefaultsToJPEG() {
        let threeBytes = Data([0x89, 0x50, 0x4E])
        XCTAssertEqual(detectImageMIMEType(threeBytes), "image/jpeg")
    }

    func testExactlyFourBytePNG() {
        // Minimum needed to detect PNG
        let pngHeader = Data([0x89, 0x50, 0x4E, 0x47])
        XCTAssertEqual(detectImageMIMEType(pngHeader), "image/png")
    }

    // MARK: - Anthropic media type detection

    func testAnthropicJPEG() {
        let jpegData = Data([0xFF, 0xD8, 0xFF, 0xE0])
        XCTAssertEqual(detectAnthropicMediaType(jpegData), .jpeg)
    }

    func testAnthropicPNG() {
        let pngData = Data([0x89, 0x50, 0x4E, 0x47])
        XCTAssertEqual(detectAnthropicMediaType(pngData), .png)
    }

    func testAnthropicGIF() {
        let gifData = Data([0x47, 0x49, 0x46, 0x38])
        XCTAssertEqual(detectAnthropicMediaType(gifData), .gif)
    }

    func testAnthropicWebP() {
        let webpData = Data([0x52, 0x49, 0x46, 0x46])
        XCTAssertEqual(detectAnthropicMediaType(webpData), .webp)
    }

    func testAnthropicEmptyDataDefaultsToJPEG() {
        XCTAssertEqual(detectAnthropicMediaType(Data()), .jpeg)
    }
}
