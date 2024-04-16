from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get, rm, rmdir
from conan.tools.microsoft import is_msvc
import os

required_conan_version = ">=1.53.0"


class RxspencerConan(ConanFile):
    name = "rxspencer"
    description = "A modified version of Henry Spencer's BSD regular expression library."
    # Use short name only, conform to SPDX License List: https://spdx.org/licenses/
    # In case not listed there, use "LicenseRef-<license-file-name>"
    license = ""
    url = "https://garyhouston.github.io/regex"
    homepage = "https://github.com/garyhouston/rxspencer"
    topics = ("regex",)
    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
        # for plain C projects only
        self.settings.rm_safe("compiler.cppstd")
        self.settings.rm_safe("compiler.libcxx")

    def layout(self):
        cmake_layout(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["rxshared"] = 1 if self.options.shared else 0
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "COPYRIGHT", self.source_folder, os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()

        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        rmdir(self, os.path.join(self.package_folder, "share"))
        rmdir(self, os.path.join(self.package_folder, "man"))
        if self.settings.os == "Windows" and is_msvc(self):
            rm(self, "*.pdb", self.package_folder, recursive=True)

    def package_info(self):
        self.cpp_info.libs = ["rxspencer"]
