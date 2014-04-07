namespace MemberQuery.Models
{
	public class QueryResults
	{
		public readonly string[] States = @"
AE
AK
AL
AP
AR
AZ
CA
CO
CT
DC
DE
FL
GA
HI
IA
ID
IL
IN
KS
KY
LA
MA
MD
ME
MI
MN
MO
MS
MT
NC
ND
NE
NH
NJ
NM
NV
NY
OH
OK
ON
OR
PA
RI
SC
SD
TN
TX
UT
VA
VT
WA
WI
WV
WY
XX".Split('\n');

		public string BirthYear { get; set; }

		public string Location { get; set; }

		public string CptCodes { get; set; }

		public TransitionPredictions Results { get; set; }
	}
}