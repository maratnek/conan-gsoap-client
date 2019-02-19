from conans import ConanFile, CMake, AutoToolsBuildEnvironment, tools, RunEnvironment
from conans.tools import download, unzip
from os import environ, unlink, getcwd, mkdir
import shutil
import platform
import os

class GSoapConan(ConanFile):
    name = environ.get("PACKAGE_NAME") if "PACKAGE_NAME" in environ else "gsoap"
    version = environ.get("PACKAGE_VERSION") if "PACKAGE_VERSION" in environ else "2.8.79"
    license = "GPLv2"
    author = "ZM"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "WITSML SOAP client service"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    # def create_soap_lib():
        # print("Create soap lib funciton")

    # def configure_cmake(self):
    #     cmake = CMake(self)
    #     cmake.definitions["DEFAULT"] = 0
    #     cmake.definitions["ENABLE_BUILD_LIB"] = 1
    #     cmake.definitions["ENABLE_BUILD_SHARED"] = 1
    #     cmake.definitions["ENABLE_CXX11"] = 1
    #     cmake.definitions["ENABLE_MESH"] = 1
    #     cmake.definitions["ENABLE_OCC"] = 1
    #     cmake.definitions["ENABLE_PARSER"] = 1
    #     cmake.definitions["ENABLE_POST"] = 1
    #     cmake.configure()
    #     return cmake

    def source(self):
        print("*************************************************************************")
        print("****************************execute source*******************************")
        print("*************************************************************************")

        # create_soap_lib()


        zip_name = self.name + "_" + self.version + ".zip"
        download("https://artifacts.devogip.ru/artifactory/gm-public/" + zip_name, zip_name)
        unzip(zip_name)
        shutil.move(self.name + "-2.8", self.name)
        unlink(zip_name)

        if platform.system() == "Linux":
            print("Linux make soapstd2 & wsdl2h")
        else:
            self.run("dir")

    def build(self):
        print("*************************************************************************")
        print("****************************execute build********************************")
        print("*************************************************************************")
        print(platform.system())
        if platform.system() == "Windows":
            print("windows")
            self.run("dir")
            path = "./gsoap/gsoap/bin/win32/"
            extension = ".exe"
            option_wsdl = " -c++11 -o witsml.h http://witsml.tpu.ru/service/wmls.asmx?WSDL";
            with tools.chdir(path):
                self.run("dir")
                self.run("wsdl2h" + extension + option_wsdl)
                mkdir("source")
                self.run("dir")
                shutil.copy("witsml.h", "./source")
                shutil.copy("../../stdsoap2.cpp ../../stdsoap2.h",  "./source")
                #soap2cpp create all files the client soap
                option_soap = " -1 -i -j -b -c++11 -g -r -T -t -C -I../../import witsml.h -d source -e -x";
                self.run("soapcpp2" + extension + option_soap)
                # Need to create CMakeLists
                with tools.chdir("./source"):
                    # shutil.copy(self.current_path + "CMakeLists.txt", ".")
                    f = open("./CMakeLists.txt", "w")
                    # contents = f.readlines()
                    self.run("dir")
                    contents =  """
                        cmake_minimum_required(VERSION 3.10)
                        project(soap_wsdl_schema)
                        set(CMAKE_CXX_FLAGS "-DWITH_NO_C_LOCALE")
                        file(GLOB_RECURSE SOAP_WSDL_SOURCE
                           "*.h"
                           "*.nsmap"
                           "*.cpp")
                        message(STATUS -- ${SOAP_WSDL_SOURCE})
                        add_library(${PROJECT_NAME} STATIC ${SOAP_WSDL_SOURCE})
                     """
                    f.write(contents)
                    f.close()
                    self.run("dir")
                    mkdir("build")

                    cmake = CMake(self)
                    cmake.configure(source_folder=path + "/source", build_folder=self.build_folder)
                    cmake.build()
                    # cmake = CMake(self)
                    # print(self.source_folder)
                    # print(cmake.command_line)
                    # print(cmake.build_config)
                    # self.run('cmake . ')
                    # self.run('cmake --build . ')
                    # self.run('cmake --build . --target install')

        else: # Linux System
            self.run("ls")
            path_wsdl = "./gsoap/gsoap/wsdl/wsdl2h";
            path_soap = "./gsoap/gsoap/src/soapstd2";
            with tools.chdir("./gsoap"):
                self.run("ls")
                env_build = AutoToolsBuildEnvironment(self, True)
                with tools.environment_append(env_build.vars):
                    self.run("chmod +x ./configure")
                    self.run("./configure --disable-ssl --bindir=$pwd/gsoap/bin/linux")
                    self.run("autoreconf -f -i")
                    self.run("make")
                with tools.chdir("./gsoap/bin"):
                    mkdir("linux")
                    print('directory')
                    self.run("pwd")
                    self.run("ls")
                    shutil.copy("../wsdl/wsdl2h", "linux")
                    shutil.copy("../src/soapcpp2", "linux")
                    self.run("ls")

        # create_soap_lib()
        print("end build conan")


    def package(self):
        print("*************************************************************************")
        print("****************************execute package******************************")
        print("*************************************************************************")

        # cmake = self.configure_cmake()
        # cmake = CMake(self)
        # cmake.install()

    def package_info(self):
        print("*************************************************************************")
        print("****************************execute package info*************************")
        print("*************************************************************************")
        self.cpp_info.libs = tools.collect_libs(self)

    # def build(self):
        # cmake = CMake(self)
        # cmake.configure(source_folder="hello")
        # cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    # def package(self):
        # self.copy("*.h", dst="include", src="hello")
        # self.copy("*hello.lib", dst="lib", keep_path=False)
        # self.copy("*.dll", dst="bin", keep_path=False)
        # self.copy("*.so", dst="lib", keep_path=False)
        # self.copy("*.dylib", dst="lib", keep_path=False)
        # self.copy("*.a", dst="lib", keep_path=False)

    # def package_info(self):
        # self.cpp_info.libs = ["hello"]
