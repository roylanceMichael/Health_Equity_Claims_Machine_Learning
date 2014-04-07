namespace MemberQuery.Resources
{
	using System;

	public static class StringUtils
	{
		public const string StartState = "START_STATE";

		public static void CheckIfArgNull(this object argument, string argumentName)
		{
			if (argument == null)
			{
				throw new ArgumentException(argumentName);
			}
		}
	}
}