#!/usr/bin/env python3
import os
import inspect
import click
import platform
import subprocess
import shutil
import glob
import itertools

from common import get_binary_arches

root = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    )
)
desktop_dir = os.path.join(root, "desktop")

identity_name_application = "Developer ID Application: Science & Design, Inc. (7WLJ4UBL5L)"
entitlements_plist_path = f"{desktop_dir}/package/Entitlements.plist"


def get_app_path():
    return os.path.join(desktop_dir, "build", "Onionetwork.app")


def run(cmd, cwd=None, error_ok=False):
    print(f"{cmd} # cwd={cwd}")
    subprocess.run(cmd, cwd=cwd, check=True)


def get_size(dir):
    size = 0
    for path, dirs, files in os.walk(dir):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)
    return size


def sign(path, entitlements, identity):
    run(
        [
            "codesign",
            "--sign",
            identity,
            "--entitlements",
            str(entitlements),
            "--timestamp",
            "--deep",
            "--force",
            "--options",
            "runtime,library",
            str(path),
        ]
    )


def get_binaries():
    pass


@click.group()
def main():
    """
    macOS build tasks
    """


@main.command()
def cleanup_build():
    """Delete unused PySide6 stuff to save space"""
    app_path = get_app_path()
    before_size = get_size(app_path)

    print("> Delete unused Qt Frameworks")
    for framework in [
        "QtMultimediaQuick",
        "QtQuickControls2",
        "QtQuickParticles",
        "QtRemoteObjects",
        "Qt3DInput",
        "QtNetworkAuth",
        "QtDataVisualization",
        "QtWebEngineCore",
        "Qt3DQuickRender",
        "Qt3DQuickExtras",
        "QtDesigner",
        "QtNfc",
        "QtQuick3DAssetImport",
        "QtWebEngineWidgets",
        "QtQuickWidgets",
        "Qt3DQuickInput",
        "Qt3DQuickScene2D",
        "Qt3DRender",
        "QtQuick3DRuntimeRender",
        "QtHelp",
        "QtPrintSupport",
        "QtCharts",
        "QtWebSockets",
        "QtQuick3DUtils",
        "QtQuickTemplates2",
        "QtPositioningQuick",
        "Qt3DCore",
        "QtXml",
        "QtSerialPort",
        "QtQuick",
        "QtScxml",
        "QtQml",
        "Qt3DExtras",
        "QtWebChannel",
        "QtMultimedia",
        "QtQmlWorkerScript",
        "QtVirtualKeyboard",
        "QtOpenGL",
        "Qt3DQuick",
        "QtTest",
        "QtPositioning",
        "QtBluetooth",
        "QtQuick3D",
        "Qt3DLogic",
        "QtQuickShapes",
        "QtQuickTest",
        "QtNetwork",
        "QtDesignerComponents",
        "QtMultimediaWidgets",
        "QtQmlModels",
        "Qt3DQuickAnimation",
        "QtSensors",
        "Qt3DAnimation",
        "QtSql",
        "QtConcurrent",
        "QtChartsQml",
        "QtDataVisualizationQml",
        "QtLabsAnimation",
        "QtLabsFolderListModel",
        "QtLabsQmlModels",
        "QtLabsSettings",
        "QtLabsSharedImage",
        "QtLabsWavefrontMesh",
        "QtOpenGLWidgets",
        "QtQmlCore",
        "QtQmlLocalStorage",
        "QtQmlXmlListModel",
        "QtQuick3DAssetUtils",
        "QtQuick3DEffects",
        "QtQuick3DGlslParser",
        "QtQuick3DHelpers",
        "QtQuick3DIblBaker",
        "QtQuick3DParticleEffects",
        "QtQuick3DParticles",
        "QtQuickControls2Impl",
        "QtQuickDialogs2",
        "QtQuickDialogs2QuickImpl",
        "QtQuickDialogs2Utils",
        "QtQuickLayouts",
        "QtQuickTimeline",
        "QtRemoteObjectsQml",
        "QtScxmlQml",
        "QtSensorsQuick",
        "QtShaderTools",
        "QtStateMachine",
        "QtStateMachineQml",
        "QtSvgWidgets",
        "QtUiTools",
        "QtWebEngineQuick",
        "QtWebEngineQuickDelegatesQml",
    ]:
        try:
            shutil.rmtree(
                f"{app_path}/Contents/MacOS/lib/PySide6/Qt/lib/{framework}.framework"
            )
            print(
                f"Deleted: {app_path}/Contents/MacOS/lib/PySide6/Qt/lib/{framework}.framework"
            )
        except FileNotFoundError:
            pass
        try:
            os.remove(f"{app_path}/Contents/MacOS/lib/PySide6/{framework}.abi3.so")
            print(f"Deleted: {app_path}/Contents/MacOS/lib/PySide6/{framework}.abi3.so")
        except FileNotFoundError:
            pass
        try:
            os.remove(f"{app_path}/Contents/MacOS/lib/PySide6/{framework}.pyi")
            print(f"Deleted: {app_path}/Contents/MacOS/lib/PySide6/{framework}.pyi")
        except FileNotFoundError:
            pass

    print("> Delete more unused PySide6 stuff to save space")
    for filename in [
        f"{app_path}/Contents/Resources/lib/PySide6/Designer.app",
        f"{app_path}/Contents/Resources/lib/PySide6/glue",
        f"{app_path}/Contents/Resources/lib/PySide6/include",
        f"{app_path}/Contents/Resources/lib/PySide6/lupdate",
        f"{app_path}/Contents/Resources/lib/PySide6/Qt/qml",
        f"{app_path}/Contents/Resources/lib/PySide6/Assistant.app",
        f"{app_path}/Contents/Resources/lib/PySide6/Linguist.app",
        f"{app_path}/Contents/Resources/lib/PySide6/lrelease",
        f"{app_path}/Contents/Resources/lib/PySide6/qmlformat",
        f"{app_path}/Contents/Resources/lib/PySide6/qmllint",
        f"{app_path}/Contents/Resources/lib/PySide6/qmlls",
        f"{app_path}/Contents/Resources/lib/QtBluetooth",
        f"{app_path}/Contents/Resources/lib/QtConcurrent",
        f"{app_path}/Contents/Resources/lib/QtDesigner",
        f"{app_path}/Contents/Resources/lib/QtNetworkAuth",
        f"{app_path}/Contents/Resources/lib/QtNfc",
        f"{app_path}/Contents/Resources/lib/QtOpenGL",
        f"{app_path}/Contents/Resources/lib/QtOpenGLWidgets",
        f"{app_path}/Contents/Resources/lib/QtPositioning",
        f"{app_path}/Contents/Resources/lib/QtQuick3D",
        f"{app_path}/Contents/Resources/lib/QtQuick3DRuntimeRender",
        f"{app_path}/Contents/Resources/lib/QtQuick3DUtils",
        f"{app_path}/Contents/Resources/lib/QtShaderTools",
        f"{app_path}/Contents/Resources/lib/QtStateMachine",
        f"{app_path}/Contents/Resources/lib/QtSvgWidgets",
        f"{app_path}/Contents/Resources/lib/QtWebChannel",
        f"{app_path}/Contents/Resources/lib/QtWebEngineCore",
        f"{app_path}/Contents/Resources/lib/QtWebEngineQuick",
        f"{app_path}/Contents/Resources/lib/QtXml",
    ]:
        if os.path.isfile(filename) or os.path.islink(filename):
            os.remove(filename)
            print(f"Deleted: {filename}")
        elif os.path.isdir(filename):
            shutil.rmtree(filename)
            print(f"Deleted: {filename}")
        else:
            print(f"Cannot delete, filename not found: {filename}")

    # Set a symlink for Qt's platforms and imageformats plugins, which seems to be necessary only on arm
    if platform.system() == "Darwin" and platform.processor() == "arm":
        platforms_target_path = os.path.join("..", "Resources", "lib", "PySide6", "Qt", "plugins", "platforms")
        platforms_symlink_path = os.path.join(app_path, "Contents", "MacOS", "platforms")

        os.symlink(platforms_target_path, platforms_symlink_path)

        imageformats_target_path = os.path.join("..", "Resources", "lib", "PySide6", "Qt", "plugins", "imageformats")
        imageformats_symlink_path = os.path.join(app_path, "Contents", "MacOS", "imageformats")
        os.symlink(imageformats_target_path, imageformats_symlink_path)


    after_size = get_size(f"{app_path}")
    freed_bytes = before_size - after_size
    freed_mb = int(freed_bytes / 1024 / 1024)
    print(f"> Freed {freed_mb} mb")


@main.command()
@click.argument("app_path")
def codesign(app_path):
    """Sign macOS binaries before packaging"""
    bin_universal, bin_silicon, bin_intel = get_binary_arches(app_path)
    binaries = bin_universal + bin_silicon + bin_intel + [app_path]

    for filename in binaries:
        sign(filename, entitlements_plist_path, identity_name_application)

    print(f"> Signed app bundle: {app_path}")


@main.command()
@click.argument("app_path")
def package(app_path):
    """Build the DMG package"""
    if not os.path.exists("/usr/local/bin/create-dmg") and not os.path.exists(
        "/opt/homebrew/bin/create-dmg"
    ):
        print("> Error: create-dmg is not installed")
        return

    print("> Create DMG")
    version_filename = f"{root}/cli/onionetwork_cli/resources/version.txt"
    with open(version_filename) as f:
        version = f.read().strip()

    os.makedirs(f"{desktop_dir}/dist", exist_ok=True)
    dmg_path = f"{desktop_dir}/dist/Onionetwork-{version}.dmg"
    run(
        [
            "create-dmg",
            "--volname",
            "Onionetwork",
            "--volicon",
            f"{desktop_dir}/onionetwork/resources/onionetwork.icns",
            "--window-size",
            "400",
            "200",
            "--icon-size",
            "100",
            "--icon",
            "Onionetwork.app",
            "100",
            "70",
            "--hide-extension",
            "Onionetwork.app",
            "--app-drop-link",
            "300",
            "70",
            dmg_path,
            app_path,
            "--identity",
            identity_name_application,
        ]
    )

    print(f"> Finished building DMG: {dmg_path}")


if __name__ == "__main__":
    main()
