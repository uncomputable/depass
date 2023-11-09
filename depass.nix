{ python3
, lib
}:
python3.pkgs.buildPythonApplication {
  pname = "depass";
  version = "0.1";

  src = ./.;

  meta = with lib; {
    description = "Deprecate passwords inside the password store";
    license = licenses.cc0;
  };
}
