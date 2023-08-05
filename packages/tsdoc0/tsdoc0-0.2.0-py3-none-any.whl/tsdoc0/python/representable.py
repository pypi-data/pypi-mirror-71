class Representable:
    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}:{v!r}" for k, v in vars(self).items() if k != "parent")

        return f"<{type(self).__name__} {attrs}>"
