from math import sqrt

def get_cdf(probabilistic):
    cdf = []
    old_item = 0
    
    for p in probabilistic:
        cdf.append(p + old_item)
        old_item += p
        
    return [round(c, 2) for c in cdf]

def represent_range(cdf):
    cdf = cdf.copy()
    cdf.insert(0, 0)
    r = []
    for i in range(len(cdf)-1):
        r.append(('{} < R <= {}'.format(cdf[i], cdf[i+1])))
    return r

def get_range(cdf):
    cdf = cdf.copy()
    cdf.insert(0, 0)
    r = []
    for i in range(len(cdf)-1):
        r.append([cdf[i], cdf[i+1]])
    return r


def get_in_range_index(rg, random):
    index = -1
    for i in range(len(rg)):
        if random >= rg[i][0] and random <= rg[i][1]:
            index = i
            return index


def create_supply_table(supply, probabilistic):

    cdf = get_cdf(probabilistic)
    rg = represent_range(cdf)

    print('                                     SUPPLY TABLE')
    print('+--------------------+--------------------+--------------------+--------------------+')
    print('|{}|{}|{}|{}|'.format('SUPPLY'.ljust(20), 'PROBABILISTIC'.ljust(20), 'CDF'.ljust(20), 'BATAS RI'.ljust(20)))
    print('+--------------------+--------------------+--------------------+--------------------+')
    
    for s, p, c, r in zip(supply, probabilistic, cdf, rg):
        print('|{}|{}|{}|{}|'.format(str(s).ljust(20),
                                     str(p).ljust(20),
                                     str(c).ljust(20),
                                     str(r).ljust(20))
              )

    print('+--------------------+--------------------+--------------------+--------------------+\n\n')


def create_demand_table(demand, probabilistic):

    cdf = get_cdf(probabilistic)
    rg = represent_range(cdf)

    print('                                    DEMAND TABLE')
    print('+--------------------+--------------------+--------------------+--------------------+')
    print('|{}|{}|{}|{}|'.format('DEMAND'.ljust(20), 'PROBABILISTIC'.ljust(20), 'CDF'.ljust(20), 'BATAS RI'.ljust(20)))
    print('+--------------------+--------------------+--------------------+--------------------+')
    
    for s, p, c, r in zip(demand, probabilistic, cdf, rg):
        print('|{}|{}|{}|{}|'.format(str(s).ljust(20),
                                     str(p).ljust(20),
                                     str(c).ljust(20),
                                     str(r).ljust(20))
              )

    print('+--------------------+--------------------+--------------------+--------------------+\n\n')


def create_benefit_calculation_table(a_year, sale_price, buy_price, fine_fees, supply, demand,
                                     supply_probabilistic, demand_probabilistic,
                                     supply_random, demand_random):

    print('{}'.format('BENEFIT CALCULATION TABLE'.rjust(75)))
    print('+---------------------------------------+---------------------------------------+---------------------------------------+')
    print('|{}|{}|{}|'.format(str('SUPPLY').ljust(39),
                              str('DEMAND').ljust(39),
                              str('REVENUE').ljust(39))
          )

    print('+---------+---------+---------+---------+---------+---------+---------+---------+------------+------------+-------------+')
    print('|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|'.format(str(1).ljust(9),
                                                      str(2).ljust(9),
                                                      str(3).ljust(9),
                                                      str(4).ljust(9),
                                                      str(5).ljust(9),
                                                      str(6).ljust(9),
                                                      str(7).ljust(9),
                                                      str(8).ljust(9),
                                                      str(9).ljust(12),
                                                      str(10).ljust(12),
                                                      str(11).ljust(13)))

    print('+---------+---------+---------+---------+---------+---------+---------+---------+------------+------------+-------------+')
    
    print('|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|'.format(str('HARI KE').ljust(9),
                                                      str('RN').ljust(9),
                                                      str('S').ljust(9),
                                                      str('COST(RP)').ljust(9),
                                                      str('RN').ljust(9),
                                                      str('D').ljust(9),
                                                      str('SALES').ljust(9),
                                                      str('REVENUE').ljust(9),
                                                      str('SHORTED COST').ljust(12),
                                                      str('STORE').ljust(12),
                                                      str('PROFIT').ljust(13)))
    
    print('+---------+---------+---------+---------+---------+---------+---------+---------+------------+------------+-------------+')


    supply_cdf = get_cdf(supply_probabilistic)
    supply_range = get_range(supply_cdf)

    demand_cdf = get_cdf(demand_probabilistic)
    demand_range = get_range(demand_cdf)

    index = 0

    penyimpanan = [0]

    sales = []

    costs = []


    profits = []

    revenues = []

    supplies = []

    demands = []

    costs_rp = []

    for sr, dr, in zip(supply_random, demand_random):
        sr_range_index = get_in_range_index(supply_range, sr) + 1
        dr_range_index = get_in_range_index(demand_range, dr) + 1

        supplies.append(sr_range_index)
        demands.append(dr_range_index)

        if (sr_range_index + penyimpanan[index]) < dr_range_index:
            sales.append(sr_range_index + penyimpanan[index])
        elif (sr_range_index + penyimpanan[index]) == dr_range_index:
            sales.append(dr_range_index)
        elif (sr_range_index + penyimpanan[index]) > dr_range_index:
            sales.append(dr_range_index)

        if (sr_range_index + penyimpanan[index]) < dr_range_index:
            cost = (dr_range_index - (sr_range_index + penyimpanan[index])) * fine_fees
            costs.append(cost)

        elif (sr_range_index + penyimpanan[index]) == dr_range_index:
            cost = 0
            costs.append(cost)
            
        elif (sr_range_index + penyimpanan[index]) > dr_range_index:
            cost = 0
            costs.append(cost)

        if (sr_range_index + penyimpanan[index]) < dr_range_index:
            penyimpanan.append(0)
        elif (sr_range_index + penyimpanan[index]) == dr_range_index:
            penyimpanan.append(0)
        elif (sr_range_index + penyimpanan[index]) > dr_range_index:
            disimpan = (sr_range_index + penyimpanan[index]) - dr_range_index
            penyimpanan.append(disimpan)

        revenue = sales[index] * sale_price
        profit = revenue - (sr_range_index * buy_price) - costs[index]

        profits.append(profit)
        revenues.append(revenue)

        costs_rp.append(sr_range_index * buy_price)

        print('|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|'.format(str(index+1).ljust(9),
                                                      str(sr).ljust(9),
                                                      str(sr_range_index).ljust(9),
                                                      str(sr_range_index * buy_price).ljust(9),
                                                      str(dr).ljust(9),
                                                      str(dr_range_index).ljust(9),
                                                      str(sales[index]).ljust(9),
                                                      str(revenue).ljust(9),
                                                      str(costs[index]).ljust(12),
                                                      str(penyimpanan[index+1]).ljust(12),
                                                      str(profit).ljust(13)))

        
            
        index += 1

        

    print('+---------+---------+---------+---------+---------+---------+---------+---------+------------+------------+-------------+')
    print('|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|'.format(str('TOTAL').ljust(9),
                                                      str(round(sum(supply_random), 14)).ljust(9),
                                                      str(sum(supplies)).ljust(9),
                                                      str(sum(costs_rp)).ljust(9),
                                                      str(sum(demand_random)).ljust(9),
                                                      str(sum(demands)).ljust(9),
                                                      str(sum(sales)).ljust(9),
                                                      str(sum(revenues)).ljust(9),
                                                      str(sum(costs)).ljust(12),
                                                      str(sum(penyimpanan)).ljust(12),
                                                      str('RP. ' + str(sum(profits))).ljust(13)))

    print('+---------+---------+---------+---------+---------+---------+---------+---------+------------+------------+-------------+\n\n\n')

    print('------------------------------------------------------------------------------------------------------------------------------')
    print('                                                2. VARIANSI DAN STANDAR DEVIASI')
    print('------------------------------------------------------------------------------------------------------------------------------\n\n')

    mean = sum(profits) / len(supply_random)

    print('A. UNTUK HARIAN')

    print('\tMEAN                =  TOTAL PROFIT / JUMLAH BILANGAN RANDOM')
    print('\t                    =  {} / {}'.format(sum(profits), len(supply_random)))
    print('\t                    =  {}\n\n'.format(mean))


    print('\tVARIANCE            =  ', end='')

    profit_mul_mean = [ ((p-mean) ** 2) for p in profits]

    for p in profits:
        print('({} - {})^2 + '.format(p, mean), end=' ')

    print('\n\t                     -----------------------------------------------------------------------')
    print('\t                       {}\n'.format(len(supply_random) - 1))

    print('\t                    =  {}'.format(sum(profit_mul_mean)))
    print('\t                       -----------------------------------------------------------------------')
    print('\t                       {}\n'.format(len(supply_random) - 1))

    variance = sum(profit_mul_mean) / (len(supply_random) - 1)

    print('\t                    =  {}\n\n'.format(variance))

    standard_deviasi = sqrt(variance)

    print('\tSTANDARD DEVIATION  =  SQRT(VARIANCE)')
    print('\t                    =  SQRT({})'.format(variance))
    print('\t                    =  {}\n\n'.format(standard_deviasi))

    print('B. UNTUK TAHUNAN\n')

    year_mean = a_year * mean
    year_variance = a_year * variance
    year_standar_deviasi = sqrt(year_variance)


    print('\tMEAN                =  JUMLAH HARI DALAM SETAHUN * MEAN HARIAN')
    print('\t                    =  {} * {}'.format(a_year, mean))
    print('\t                    =  {}\n\n'.format(year_mean))
    
    print('\tVARIANCE            =  JUMLAH HARI DALAM SETAHUN * VARIANCE HARIAN')
    print('\t                    =  {} * {}'.format(a_year, variance))
    print('\t                    =  {}\n\n'.format(year_variance))


    print('\tSTANDARD DEVIATION  =  SQRT(VARIANCE TAHUNAN)')
    print('\t                    =  SQRT({})'.format(year_variance))
    print('\t                    =  {}\n\n'.format(year_standar_deviasi))


def demo():
    supply = [
        1,
        2,
        3,
        4,
        5
    ]

    supply_probabilistic = [
        0.31,
        0.27,
        0.21,
        0.16,
        0.05
    ]

    demand = [
        1,
        2,
        3,
        4,
        5,
    ]

    demand_probabilistic = [
        0.1,
        0.2,
        0.4,
        0.2,
        0.1,
    ]

    supply_random = [
         0.88, 0.47, 0.90, 0.35, 0.22, 0.48, 0.58, 0.42, 0.66, 0.08
    ]

    demand_random = [
         0.52, 0.27, 0.06, 0.94, 0.15, 0.62, 0.14, 0.71, 0.12, 0.6
    ]

    buy_price = 50 # 10 per unit
    sale_price = 100 # 20 per unit
    fine_fees = 20 # 5 per unit
    a_year = 180 # 289 days
    
    print('\nDIKETAHUI : \n')
    print('\tHARGA BELI  =  RP. {} / UNIT'.format(buy_price))
    print('\tHARGA JUAL  =  RP. {} / UNIT'.format(sale_price))
    print('\tDENDA       =  RP. {} / UNIT'.format(fine_fees))
    print('\t1 TAHUN     =  {} HARI\n\n'.format(a_year))


    print('------------------------------------------------------------------------------------------------------------------------------')
    print('                             1. SIMULASI {} HARI TRANSAKSI DAN KEUNTUNGAN SETIAP HARI'.format(str(len(supply_random))))
    print('------------------------------------------------------------------------------------------------------------------------------\n\n')

    


    create_supply_table(supply, supply_probabilistic)
    create_demand_table(demand, demand_probabilistic)
    create_benefit_calculation_table(a_year, sale_price, buy_price, fine_fees, supply, demand,
                                     supply_probabilistic, demand_probabilistic,
                                     supply_random, demand_random)


if __name__ == '__main__':
    demo()