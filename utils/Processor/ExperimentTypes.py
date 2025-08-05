class ExperimentTypes:
    
    TENSILE = 0
    BENDING = 1

    @classmethod
    def get_recipient( cls, mode : int ):
        if mode == ExperimentTypes.TENSILE:
            return {
                "engineer" : {
                    "strain"  : [],
                    "stress"  : []
                },
                "real" : {
                    "strain" : [],
                    "stress" : []
                }
            }
        elif mode == ExperimentTypes.BENDING:
            return {
                "D790" : {
                    "strain" : [],
                    "stress" : []
                },
                "custom/3PB-theory" : {
                    "strain" : [],
                    "stress" : []
                }
            }

    @classmethod
    def read_results( cls, data, datum : tuple[ float, ... ], mode : int ):
        if mode == ExperimentTypes.TENSILE:
            es, eS, rs, rS = datum
            data["engineer"]["strain"].append( es )
            data["engineer"]["stress"].append( eS )
            data["real"]["strain"].append( rs )
            data["real"]["stress"].append( rS )
        elif mode == ExperimentTypes.BENDING:
            ds, dS, cs, cS = datum
            data["D790"]["strain"].append( ds )
            data["D790"]["stress"].append( dS )
            data["custom/3PB-theory"]["strain"].append( cs )
            data["custom/3PB-theory"]["stress"].append( cS )


