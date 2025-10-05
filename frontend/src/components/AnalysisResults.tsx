import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { TrendingDown, TrendingUp, ShoppingCart } from 'lucide-react'

interface TopItem {
  description: string
  amount: number
  date: string
}

interface ChartData {
  date: string
  debits: number
  credits: number
}

interface Merchant {
  name: string
  amount: number
}

interface Category {
  category: string
  total_amount: number
  transaction_count: number
  top_merchants: Merchant[]
}

interface FileResult {
  file_name: string
  transaction_count: number
  total_debits: number
  total_credits: number
  top_expenses: TopItem[]
  top_revenues: TopItem[]
  chart_data: ChartData[]
  spending_by_category: Category[]
}

interface AnalysisResultsProps {
  results: {
    files_processed: number
    results: FileResult[]
  }
  onReset: () => void
}

export const AnalysisResults: React.FC<AnalysisResultsProps> = ({ results, onReset }) => {
  const fileResult = results.results[0]

  return (
    <div className="w-full max-w-6xl mx-auto p-6 space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-red-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Debits</p>
              <p className="text-3xl font-bold text-red-600">
                €{fileResult.total_debits.toLocaleString('de-DE', { minimumFractionDigits: 2 })}
              </p>
              <p className="text-sm text-gray-500 mt-1">
                {fileResult.transaction_count} transactions
              </p>
            </div>
            <TrendingDown className="h-12 w-12 text-red-500" />
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-green-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Credits</p>
              <p className="text-3xl font-bold text-green-600">
                €{fileResult.total_credits.toLocaleString('de-DE', { minimumFractionDigits: 2 })}
              </p>
              <p className="text-sm text-gray-500 mt-1">
                Net: €{(fileResult.total_credits - fileResult.total_debits).toLocaleString('de-DE', { minimumFractionDigits: 2 })}
              </p>
            </div>
            <TrendingUp className="h-12 w-12 text-green-500" />
          </div>
        </div>
      </div>

      {/* Spending by Category */}
      {fileResult.spending_by_category && fileResult.spending_by_category.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4 flex items-center">
            <ShoppingCart className="h-6 w-6 text-blue-500 mr-2" />
            Top Spending by Category
          </h3>
          <div className="space-y-6">
            {fileResult.spending_by_category.map((category, idx) => (
              <div key={idx} className="border-l-4 border-blue-500 pl-4">
                <div className="flex justify-between items-center mb-2">
                  <h4 className="font-semibold text-gray-900">{category.category}</h4>
                  <span className="text-lg font-bold text-blue-600">
                    €{category.total_amount.toLocaleString('de-DE', { minimumFractionDigits: 2 })}
                  </span>
                </div>
                <p className="text-sm text-gray-500 mb-3">
                  {category.transaction_count} transactions
                </p>
                <div className="space-y-2">
                  {category.top_merchants.map((merchant, midx) => (
                    <div key={midx} className="flex justify-between items-center bg-gray-50 p-2 rounded">
                      <span className="text-sm text-gray-700">{midx + 1}. {merchant.name}</span>
                      <span className="text-sm font-medium text-gray-900">
                        €{merchant.amount.toLocaleString('de-DE', { minimumFractionDigits: 2 })}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Cumulative Line Chart */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-xl font-semibold mb-4">Cumulative Debits vs Credits Over Time</h3>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={fileResult.chart_data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis 
              dataKey="date" 
              tick={{ fontSize: 12 }}
              angle={-45}
              textAnchor="end"
              height={80}
            />
            <YAxis 
              tick={{ fontSize: 12 }}
              tickFormatter={(value) => `€${value}`}
            />
            <Tooltip 
              formatter={(value: number) => `€${value.toLocaleString('de-DE', { minimumFractionDigits: 2 })}`}
              contentStyle={{ backgroundColor: '#fff', border: '1px solid #ccc' }}
            />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="debits" 
              stroke="#ef4444" 
              strokeWidth={3}
              name="Cumulative Debits"
              dot={{ fill: '#ef4444', r: 5 }}
              activeDot={{ r: 7 }}
            />
            <Line 
              type="monotone" 
              dataKey="credits" 
              stroke="#10b981" 
              strokeWidth={3}
              name="Cumulative Credits"
              dot={{ fill: '#10b981', r: 5 }}
              activeDot={{ r: 7 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Top Expenses and Revenues */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4 flex items-center">
            <TrendingDown className="h-6 w-6 text-red-500 mr-2" />
            Top 3 Expenses
          </h3>
          <div className="space-y-3">
            {fileResult.top_expenses.map((expense, index) => (
              <div key={index} className="p-4 bg-red-50 rounded-lg border border-red-100">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">
                      {index + 1}. {expense.description.substring(0, 50)}
                      {expense.description.length > 50 ? '...' : ''}
                    </p>
                    <p className="text-sm text-gray-500 mt-1">{expense.date}</p>
                  </div>
                  <p className="text-lg font-bold text-red-600 ml-2">
                    €{expense.amount.toLocaleString('de-DE', { minimumFractionDigits: 2 })}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-xl font-semibold mb-4 flex items-center">
            <TrendingUp className="h-6 w-6 text-green-500 mr-2" />
            Top 3 Revenues
          </h3>
          <div className="space-y-3">
            {fileResult.top_revenues.map((revenue, index) => (
              <div key={index} className="p-4 bg-green-50 rounded-lg border border-green-100">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">
                      {index + 1}. {revenue.description.substring(0, 50)}
                      {revenue.description.length > 50 ? '...' : ''}
                    </p>
                    <p className="text-sm text-gray-500 mt-1">{revenue.date}</p>
                  </div>
                  <p className="text-lg font-bold text-green-600 ml-2">
                    €{revenue.amount.toLocaleString('de-DE', { minimumFractionDigits: 2 })}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Reset Button */}
      <button
        onClick={onReset}
        className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium"
      >
        Analyze More Statements
      </button>
    </div>
  )
}
