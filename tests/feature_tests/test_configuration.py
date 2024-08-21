from cyberfusion.FermSupport.configuration import Configuration


def test_configuration_string_variable(configuration: Configuration) -> None:
    configuration.add_variable(name="test", values=["a", "b", "c"])

    assert (
        str(configuration)
        == """@def $TEST = (
  a
  b
  c
);
"""
    )


def test_configuration_string_custom_line(
    configuration: Configuration,
) -> None:
    LINE = "proto (tcp) dport 22 saddr @ipfilter($MANAGEMENT) ACCEPT;"

    configuration.add_custom_line(contents=LINE)

    assert str(configuration) == LINE + "\n"
