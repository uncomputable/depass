{ python3
, lib
}:
python3.pkgs.buildPythonApplication {
  pname = "depass";
  version = "1.0";

  src = ./.;

  meta = with lib; {
    description = "Deprecate passwords inside the password store";
    license = licenses.cc0;
  };
}
