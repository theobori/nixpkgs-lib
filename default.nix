{
  lib,
  buildPythonPackage,
  setuptools,
  pytestCheckHook,
  beautifultable,
  setuptools-scm,
}:
buildPythonPackage {
  pname = "nixpkgs-lib";
  version = "0.0.1";
  pyproject = true;

  src = ./.;

  build-system = [
    setuptools
    setuptools-scm
  ];

  dependencies = [
    beautifultable
  ];

  nativeCheckInputs = [ pytestCheckHook ];

  pythonImportsCheck = [ "nixpkgs_lib" ];

  meta = {
    description = "Nixpkgs library part implementation in Python with laziness simulation";
    homepage = "https://github.com/theobori/nixpkgs-lib";
    license = lib.licenses.mit;
    mainProgram = "statistics";
  };
}
