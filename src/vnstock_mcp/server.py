from vnstock import Quote
from vnstock.explorer.tcbs.company import Company as TCBSCompany
from vnstock.explorer.vci.company import Company as VCICompany
from vnstock.explorer.vci.listing import Listing as VCIListing
from vnstock.explorer.vci.financial import Finance as VCIFinance
from vnstock.explorer.fmarket.fund import Fund as FMarketFund
from vnstock.explorer.misc.gold_price import sjc_gold_price, btmc_goldprice
from vnstock.explorer.misc.exchange_rate import vcb_exchange_rate
from vnstock.explorer.vci.trading import Trading as VCITrading
from mcp.server.fastmcp import FastMCP
import pandas as pd
from typing import Literal
from datetime import datetime
import argparse
import sys

server = FastMCP('VNStock MCP Server')

##### Company Tools #####

@server.tool()
def get_company_overview(symbol: str, output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get company overview from stock market
    Args:
        symbol: str
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    equity = TCBSCompany(symbol=symbol)
    df = equity.overview()
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_company_news(symbol: str, page_size: int = 10, page: int = 0, output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get company news from stock market
    Args:
        symbol: str
        page_size: int = 10
        page: int = 0
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    equity = TCBSCompany(symbol=symbol)
    df = equity.news(page_size=page_size, page=page)
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_company_events(symbol: str, page_size: int = 10, page: int = 0, output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get company events from stock market
    Args:
        symbol: str
        page_size: int = 10
        page: int = 0
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    equity = TCBSCompany(symbol=symbol)
    df = equity.events(page_size=page_size, page=page)
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_company_shareholders(symbol: str, output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get company shareholders from stock market
    Args:
        symbol: str
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    equity = TCBSCompany(symbol=symbol)
    df = equity.shareholders()
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_company_officers(symbol: str, filter_by: Literal['working', "all", 'resigned']= 'working', output_format: Literal['json', 'dataframe'] = 'json'):  # pyright: ignore[reportUndefinedVariable]  # noqa: E501
    """
    Get company officers from stock market
    Args:
        symbol: str
        filter_by: Literal['working', "all", 'resigned'] = 'working'
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    equity = TCBSCompany(symbol=symbol)
    df = equity.officers(filter_by=filter_by)
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_company_subsidiaries(symbol: str, filter_by: Literal["all", "subsidiary"] = "all", output_format: Literal['json', 'dataframe'] = 'json'):  # pyright: ignore[reportUndefinedVariable]
    """
    Get company subsidiaries from stock market
    Args:
        symbol: str
        filter_by: Literal["all", "subsidiary"] = "all"
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    equity = TCBSCompany(symbol=symbol)
    df = equity.subsidiaries(filter_by=filter_by)
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_company_reports(symbol: str, output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get company reports from stock market
    Args:
        symbol: str
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    equity = VCICompany(symbol=symbol)
    df = equity.reports()
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_company_dividends(symbol: str, output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get company dividends from stock market
    Args:
        symbol: str
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    equity = TCBSCompany(symbol=symbol)
    df = equity.dividends()
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_company_insider_deals(symbol: str, output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get company insider deals from stock market
    Args:
        symbol: str
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    equity = TCBSCompany(symbol=symbol)
    df = equity.insider_deals()
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_company_ratio_summary(symbol: str, output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get company ratio summary from stock market
    Args:
        symbol: str
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    equity = VCICompany(symbol=symbol)
    df = equity.ratio_summary()
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_company_trading_stats(symbol: str, output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get company trading stats from stock market
    Args:
        symbol: str
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    equity = VCICompany(symbol=symbol)
    df = equity.trading_stats()
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df


##### Listing Tools #####
@server.tool()
def get_all_symbol_groups(output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get all symbol groups from stock market
    Args:
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    df = pd.DataFrame([{
        'group': 'HOSE',
        'group_name': 'All symbols in HOSE'
    },
    {   
        'group': 'HNX',
        'group_name': 'All symbols in HNX'
    },
    {
        'group': 'UPCOM',
        'group_name': 'All symbols in UPCOM'
    },
    {
        'group': 'VN30',
        'group_name': 'All symbols in VN30'
    },
    {
        'group': 'VN100',
        'group_name': 'All symbols in VN100'
    },
    {
        'group': 'HNX30',
        'group_name': 'All symbols in HNX30'
    },
    {
        'group': 'VNMidCap',
        'group_name': 'All symbols in VNMidCap'
    },
    {
        'group': 'VNSmallCap',
        'group_name': 'All symbols in VNSmallCap'
    },
    {
        'group': 'VNAllShare',
        'group_name': 'All symbols in VNAllShare'
    },
    {
        'group': 'HNXCon',
        'group_name': 'All symbols in HNXCon'
    },
    {
        'group': 'HNXFin',
        'group_name': 'All symbols in HNXFin'
    },
    {
        'group': 'HNXLCap',
        'group_name': 'All symbols in HNXLCap'
    },
    {
        'group': 'HNXMSCap',
        'group_name': 'All symbols in HNXMSCap'
    },
    {
        'group': 'HNXMan',
        'group_name': 'All symbols in HNXMan'
    },
    {
        'group': 'ETF',
        'group_name': 'All symbols in ETF'
    },
    {
        'group': 'FU_INDEX',
        'group_name': 'All symbols in FU_INDEX'
    },
    {
        'group': 'CW',
        'group_name': 'All symbols in CW'
    }
    ])
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_all_industries(output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get all symbols from stock market
    Args:
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame or json
    """
    listing = VCIListing()
    df = listing.industries_icb()
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_all_symbols_by_group(group: str, output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get all symbols from stock market
    Args:
        group: str (group name to get symbols)
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    listing = VCIListing()
    df = listing.symbols_by_group(group=group)
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_all_symbols_by_industry(industry: str = None, output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get all symbols from stock market
    Args:
        industry: str = None (if None, return all symbols)
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame or json
    """
    listing = VCIListing()
    df = listing.symbols_by_industries()
    if industry:
        codes = ['icb_code1', 'icb_code2', 'icb_code3', 'icb_code4']
        masks = []
        for col in codes:
            if col in df.columns:
                masks.append(df[col].astype(str) == industry)
        if masks:
            mask = masks[0]
            for m in masks[1:]:
                mask = mask | m
            df = df[mask]
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_all_symbols(output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get all symbols from stock market
    Args:
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame or json
    """
    listing = VCIListing()
    df = listing.symbols_by_exchange()
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

##### Finance Tools #####

@server.tool()
def get_income_statements(symbol: str, period: Literal['quarter', 'year'] = 'year', output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get income statements of a company from stock market
    Args:   
        symbol: str (symbol of the company to get income statements)
        period: Literal['quarter', 'year'] = 'year' (period to get income statements)
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    finance = VCIFinance(symbol=symbol, period=period)
    df = finance.income_statement()
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_balance_sheets(symbol: str, period: Literal['quarter', 'year'] = 'year', output_format: Literal['json', 'dataframe'] = 'json'):  # pyright: ignore[reportUndefinedVariable]
    """
    Get balance sheets of a company from stock market
    Args:
        symbol: str (symbol of the company to get balance sheets)
        period: Literal['quarter', 'year'] = 'year' (period to get balance sheets)
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    finance = VCIFinance(symbol=symbol, period=period)
    df = finance.balance_sheet()
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_cash_flows(symbol: str, period: Literal['quarter', 'year'] = 'year', output_format: Literal['json', 'dataframe'] = 'json'):  # pyright: ignore[reportUndefinedVariable]
    """
    Get cash flows of a company from stock market
    Args:
        symbol: str (symbol of the company to get cash flows)
        period: Literal['quarter', 'year'] = 'year' (period to get cash flows)
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    finance = VCIFinance(symbol=symbol, period=period)
    df = finance.cash_flow()
    return df

@server.tool()
def get_finance_ratios(symbol: str, period: Literal['quarter', 'year'] = 'year', output_format: Literal['json', 'dataframe'] = 'json'):  # pyright: ignore[reportUndefinedVariable]
    """
    Get finance ratios of a company from stock market
    Args:
        symbol: str (symbol of the company to get finance ratios)
        period: Literal['quarter', 'year'] = 'year' (period to get finance ratios)
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    finance = VCIFinance(symbol=symbol, period=period)
    df = finance.ratio()
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_raw_report(symbol: str, period: Literal['quarter', 'year'] = 'year', output_format: Literal['json', 'dataframe'] = 'json'):  # pyright: ignore[reportUndefinedVariable]
    """
    Get raw report of a company from stock market
    Args:
        symbol: str (symbol of the company to get raw report)
        period: Literal['quarter', 'year'] = 'year' (period to get raw report)
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    finance = VCIFinance(symbol=symbol, period=period)
    df = finance._get_report(mode='raw')
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

##### Fund Tools #####

@server.tool()
def list_all_funds(fund_type: Literal['BALANCED', 'BOND', 'STOCK', None ] = None, output_format: Literal['json', 'dataframe'] = 'json'):  # pyright: ignore[reportUndefinedVariable]
    """
    List all funds from stock market
    Args:
        fund_type: Literal['BALANCED', 'BOND', 'STOCK', None ] = None (if None, return funds in all types)
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    fund = FMarketFund()
    df = fund.listing(fund_type=fund_type)
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def search_fund(keyword: str, output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Search fund by name from stock market
    Args:
        keyword: str (partial match for fund name to search)
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    fund = FMarketFund()
    df = fund.filter(symbol=keyword)
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_fund_nav_report(symbol: str, output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get nav report of a fund from stock market
    Args:
        symbol: str (symbol of the fund to get nav report)
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    fund = FMarketFund()
    df = fund.details.nav_report(symbol=symbol)
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_fund_top_holding(symbol: str, output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get top holding of a fund from stock market
    Args:
        symbol: str (symbol of the fund to get top holding)
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    fund = FMarketFund()
    df = fund.details.top_holding(symbol=symbol)
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_fund_industry_holding(symbol: str, output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get industry holding of a fund from stock market
    Args:
        symbol: str (symbol of the fund to get industry holding)
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    fund = FMarketFund()
    df = fund.details.industry_holding(symbol=symbol)
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_fund_asset_holding(symbol: str, output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get asset holding of a fund from stock market
    Args:
        symbol: str (symbol of the fund to get asset holding)
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    fund = FMarketFund()
    df = fund.details.asset_holding(symbol=symbol)
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

##### MISC Tools #####

@server.tool()
def get_gold_price(date: str = None, source: Literal['SJC', 'BTMC'] = 'SJC', output_format: Literal['json', 'dataframe'] = 'json'):  # pyright: ignore[reportUndefinedVariable]  # noqa: F821
    """
    Get gold price from stock market
    Args:
        date: str = None (if None, return today's price. Format: YYYY-MM-DD)
        source: Literal['SJC', 'BTMC'] = 'SJC' (source to get gold price)
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    if date:
        price = sjc_gold_price(date=date)
        if output_format == 'json':
            return price.to_json(orient='records', force_ascii=False)
        else:
            return price
    else:
        price = sjc_gold_price() if source == 'SJC' else btmc_goldprice()
        if output_format == 'json':
            return price.to_json(orient='records', force_ascii=False)
        else:
            return price

@server.tool()
def get_exchange_rate(date: str = None, output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get exchange rate of all currency pairs from stock market
    Args:
        date: str = None (if None, return today's price. Format: YYYY-MM-DD)
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    price = vcb_exchange_rate(date=date)
    if output_format == 'json':
        return price.to_json(orient='records', force_ascii=False)
    else:
        return price

##### Quote Tools #####

@server.tool()
def get_quote_history_price(symbol: str, start_date: str, end_date: str = None, interval: Literal['1m', '5m', '15m', '30m', '1H', '1D', '1W', '1M'] = '1D', output_format: Literal['json', 'dataframe'] = 'json'):  # pyright: ignore[reportUndefinedVariable]  # noqa: F722
    """
    Get quote price history of a symbol from stock market
    Args:
        symbol: str (symbol to get history price)
        start_date: str (format: YYYY-MM-DD)
        end_date: str = None (end date to get history price. None means today)
        interval: Literal['1m', '5m', '15m', '30m', '1H', '1D', '1W', '1M'] = '1D' (interval to get history price)
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    quote = Quote(symbol=symbol, source='VCI')
    df = quote.history(start_date=start_date, end_date=end_date or datetime.now().strftime('%Y-%m-%d'), interval=interval)
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_quote_intraday_price(symbol: str, page_size: int = 100, last_time: str = None, output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get quote intraday price from stock market
    Args:
        symbol: str (symbol to get intraday price)
        page_size: int = 500 (max: 100000) (number of rows to return)
        last_time: str = None (last time to get intraday price from)
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    quote = Quote(symbol=symbol, source='VCI')
    df = quote.intraday(page_size=page_size, last_time=last_time)
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

@server.tool()
def get_quote_price_depth(symbol: str, output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get quote price depth from stock market
    Args:
        symbol: str (symbol to get price depth)
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    quote = Quote(symbol=symbol, source='VCI')
    df = quote.price_depth()
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df

##### Trading Tools #####

@server.tool()
def get_price_board(symbols: list[str], output_format: Literal['json', 'dataframe'] = 'json'):
    """
    Get price board from stock market
    Args:
        symbols: list[str] (list of symbols to get price board)
        output_format: Literal['json', 'dataframe'] = 'json'
    Returns:
        pd.DataFrame
    """
    trading = VCITrading()
    df = trading.price_board(symbols_list=symbols)
    if output_format == 'json':
        return df.to_json(orient='records', force_ascii=False)
    else:
        return df


def main():
    """Main entry point for the vnstock-mcp-server CLI."""
    parser = argparse.ArgumentParser(
        description='VNStock MCP Server - Vietnam Stock Market Data Access via MCP',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
            %(prog)s                              # Run with default stdio transport
            %(prog)s --transport stdio            # Explicitly use stdio transport
            %(prog)s --transport sse              # Use Server-Sent Events transport
            %(prog)s --transport sse --mount-path /vnstock  # SSE with custom mount path
            %(prog)s --transport streamable-http  # Use HTTP streaming transport
            
            Transport Modes:
            stdio          : Standard input/output (default, for MCP clients like Claude Desktop)
            sse            : Server-Sent Events (for web applications)
            streamable-http: HTTP streaming (for HTTP-based integrations)
        """
    )
    
    parser.add_argument(
        '--transport', '-t',
        choices=['stdio', 'sse', 'streamable-http'],
        default='stdio',
        help='Transport protocol to use (default: stdio)'
    )
    
    parser.add_argument(
        '--mount-path', '-m',
        type=str,
        default=None,
        help='Mount path for SSE transport (optional, used only with --transport sse)'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    try:
        args = parser.parse_args()
        
        # Validate arguments
        if args.transport == 'sse' and args.mount_path is None:
            print("Warning: Using SSE transport without mount-path. Default mount path will be used.", file=sys.stderr)
        
        if args.transport != 'sse' and args.mount_path is not None:
            print("Warning: --mount-path is only used with SSE transport. Ignoring mount-path.", file=sys.stderr)
        
        # Run server with specified transport
        print(f"Starting VNStock MCP Server with {args.transport} transport...", file=sys.stderr)
        if args.transport == 'sse' and args.mount_path:
            print(f"SSE mount path: {args.mount_path}", file=sys.stderr)
        
        server.run(transport=args.transport, mount_path=args.mount_path)
        
    except KeyboardInterrupt:
        print("\nServer stopped by user.", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()