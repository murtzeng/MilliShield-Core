#include <iostream>
#include <string>

namespace android::millishield {

enum class ContentCategory {
    SAFE,
    VERTICAL_SHORT_VIDEO,
    RESTRICTED_CONTENT
};

class EdgeNPUClassifier {
public:
    EdgeNPUClassifier() {
        std::cout << "[MilliShield-NPU] INT8 Quantized Model Loaded into NPU Buffer." << std::endl;
    }

    ContentCategory classifyFrame(const std::string& appPackageName, float aspectRatio) {
        if (aspectRatio >= 0.50f && aspectRatio <= 0.60f) {
            std::cout << "[MilliShield-NPU] Classification Result: Dikey Video / Bağımlılık Yapan Akış Tespiti!" << std::endl;
            return ContentCategory::VERTICAL_SHORT_VIDEO;
        }
        return ContentCategory::SAFE;
    }

    void enforceSurfaceAction(ContentCategory category) {
        if (category == ContentCategory::VERTICAL_SHORT_VIDEO) {
            std::cout << "[MilliShield-AOSP] SurfaceFlinger Action: SCREEN OVERLAY APPLIED (Frame Suppressed / Blackout)." << std::endl;
        } else {
            std::cout << "[MilliShield-AOSP] SurfaceFlinger Action: FRAME PASSED (Normal Render)." << std::endl;
        }
    }
};

} // namespace android::millishield

int main() {
    using namespace android::millishield;
    EdgeNPUClassifier npu;

    std::cout << "\n--- TEST 1: Yatay Video (Youtube Normal - 16:9) ---" << std::endl;
    auto cat1 = npu.classifyFrame("com.google.android.youtube", 1.77f);
    npu.enforceSurfaceAction(cat1);

    std::cout << "\n--- TEST 2: Dikey Video (Instagram Reels / Shorts - 9:16) ---" << std::endl;
    auto cat2 = npu.classifyFrame("com.instagram.android", 0.5625f);
    npu.enforceSurfaceAction(cat2);

    return 0;
}
