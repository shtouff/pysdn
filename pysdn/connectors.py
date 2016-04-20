
class Connector(object):

    # fiber connectors
    LC = 100
    SC = 101
    FC = 102
    # copper connectors
    RJ45 = 103
    DB9 = 104
    DB25 = 105
    # power connector
    C13 = 106

    # transceivers
    GBIC = 200
    SFP = 201
    SFPPLUS = 202
    XFP = 203
    QSFP = 204

    def known_connectors():
        return (Connector.LC,
                Connector.SC,
                Connector.FC,
                Connector.RJ45,
                Connector.DB9,
                Connector.DB25,
                Connector.C13,

                Connector.GBIC,
                Connector.SFP,
                Connector.SFPPLUS,
                Connector.XFP,
                Connector.QSFP,
                )

