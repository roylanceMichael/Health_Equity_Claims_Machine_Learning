namespace MemberQuery.Models
{
	using System;
	using System.Collections.Generic;
	using System.Linq;

	using MemberQuery.Resources;

	public class TransitionEmissions
	{
		private readonly TransitionRecord transitionRecord;

		private readonly IEnumerable<EmissionRecord> emissionRecords;

		private readonly double expectedValue;

		private readonly double standardDeviation;

		private readonly double minAmount;

		private readonly double maxAmount;

		private readonly double averageAmount;
 
		public TransitionEmissions(TransitionRecord transitionRecord, IEnumerable<EmissionRecord> emissionRecords)
		{
			this.transitionRecord = transitionRecord;
			if (!emissionRecords.Any())
			{
				throw new InvalidOperationException("emissions need to have more than one value");
			}

			this.emissionRecords = emissionRecords.OrderByDescending(record => record.Probability);
			this.expectedValue = this.emissionRecords.Sum(record => record.Probability * record.TotalAmount);
			this.standardDeviation = this.emissionRecords.Select(record => record.TotalAmount).StdDev();
			this.minAmount = this.emissionRecords.Min(record => record.TotalAmount);
			this.maxAmount = this.emissionRecords.Max(record => record.TotalAmount);
			this.averageAmount = this.emissionRecords.Average(record => record.TotalAmount);
		}

		public string FromTransition
		{
			get
			{
				return this.transitionRecord.FromTransition;
			}
		}

		public string ToTransition
		{
			get
			{
				return this.transitionRecord.ToTransition;
			}
		}

		public double Probability
		{
			get
			{
				return this.transitionRecord.Probability;
			}
		}

		public string Emission
		{
			get
			{
				return this.emissionRecords.First().CptCode;
			}
		}

		public double ExpectedValue
		{
			get
			{
				return this.expectedValue;
			}
		}

		public double HighestProbabilityAmount
		{
			get
			{
				return this.emissionRecords.First().TotalAmount;
			}
		}

		public double LowestProbabilityAmount
		{
			get
			{
				return this.emissionRecords.Last().TotalAmount;
			}
		}

		public double StandardDeviation
		{
			get
			{
				return this.standardDeviation;
			}
		}

		public double MinAmount
		{
			get
			{
				return this.minAmount;
			}
		}

		public double MaxAmount
		{
			get
			{
				return this.maxAmount;
			}
		}

		public double AverageAmount
		{
			get
			{
				return this.averageAmount;
			}
		}
	}
}