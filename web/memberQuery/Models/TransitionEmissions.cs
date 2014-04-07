namespace MemberQuery.Models
{
	using System;
	using System.Collections.Generic;
	using System.Linq;

	using MemberQuery.Resources;

	public class TransitionEmissions
	{
		private readonly IEnumerable<EmissionRecord> emissionRecords;

		public TransitionEmissions(TransitionRecord transitionRecord, IEnumerable<EmissionRecord> emissionRecords)
		{
			if (transitionRecord == null || emissionRecords == null)
			{
				return;
			}

			this.FromTransition = transitionRecord.FromTransition;
			this.ToTransition = transitionRecord.ToTransition;
			this.Probability = transitionRecord.Probability;
			this.emissionRecords = emissionRecords.OrderByDescending(record => record.Probability);
			this.Emission = this.emissionRecords.First().CptCode;
			this.ExpectedValue = this.emissionRecords.Sum(record => record.Probability * record.TotalAmount);
			this.StandardDeviation = this.emissionRecords.Select(record => record.TotalAmount).StdDev();
			this.HighestProbabilityAmount = this.emissionRecords.First().TotalAmount;
			this.LowestProbabilityAmount = this.emissionRecords.Last().TotalAmount;
			this.MinAmount = this.emissionRecords.Min(record => record.TotalAmount);
			this.MaxAmount = this.emissionRecords.Max(record => record.TotalAmount);
			this.AverageAmount = this.emissionRecords.Average(record => record.TotalAmount);
		}

		public string FromTransition { get; set; }

		public string ToTransition { get; set; }

		public double Probability { get; set; }

		public string Emission { get; set; }

		public double ExpectedValue { get; set; }

		public double HighestProbabilityAmount { get; set; }

		public double LowestProbabilityAmount { get; set; }

		public double StandardDeviation { get; set; }

		public double MinAmount { get; set; }

		public double MaxAmount { get; set; }

		public double AverageAmount { get; set; }
	}
}