namespace MemberQuery.Resources
{
	using System;

	public static class StringUtils
	{
		public static void CheckIfArgNull(this string argument, string argumentName)
		{
			if (argument == null)
			{
				throw new ArgumentException(argumentName);
			}
		}
	}
}