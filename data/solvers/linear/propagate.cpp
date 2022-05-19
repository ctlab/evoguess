#include <vector>
#include <set>
#include <map>
#include <random>
#include <mutex>
#include <iostream>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <string>

using namespace std;

/// УРАВНЕНИЕ and: x ^ y & z = 0 ( x = y & z ).
/// ПОД x, y, z ПОНИМАЮТСЯ ЛИТЕРАЛЫ С НОМЕРАМИ x, y, z.
/// В СООТВЕТСТВИИ С ФОРМАТОМ AIG ПЕРЕМЕННОЙ ПОД НОМЕРОМ x
/// СТАВИТСЯ В СООТВЕТСТВИЕ ЧИСЛО 2*x, А ЕЁ ОТРИЦАНИЮ - 2*x+1.
class AndEquation
{
public:
	int x;
	int y;
	int z;

	AndEquation();
	AndEquation(int x, int y, int z);
};

AndEquation::AndEquation() {}
AndEquation::AndEquation(int x, int y, int z): x(x), y(y), z(z) {}

/// ПЕРЕЧИСЛЕНИЕ СТАТУСОВ
enum Statuses
{
    SOLVED,
    UNSOLVED,
    ERROR,
    NEW_INFO,
    NOTHING_NEW
};

/// МАССИВ КВАДРАТИЧНЫХ УРАВНЕНИЙ
vector<AndEquation> and_equations;

/// МНОЖЕСТВО ШАБЛОННЫХ ЛИНЕЙНЫХ ОГРАНИЧЕНИЙ.
/// ЛИНЕЙНОЕ ОГРАНИЧЕНИЕ - МАССИВ СЛАГАЕМЫХ ЛИТЕРАЛОВ,
/// КАК В ФОРМАТЕ AIG.
set<vector<int>> pattern_linear_constraints;

/// ТАБЛИЦА ШАБЛОННЫХ ДИЗЪЮНКТОВ.
/// КЛЮЧ - СПИСОК ПЕРЕМЕННЫХ,
/// ЗНАЧЕНИЕ - МНОЖЕСТВО ВЕКТОРОВ ОТРИЦАНИЙ.
/// ПРИМЕР.
/// [2, 4]: {[0, 0], [0, 1]}
/// СООТВЕТСТВУЕТ ДИЗЪЮНКТАМ В ФОРМАТЕ DIMACS
/// 1 2 0
/// 1 -2 0
map<vector<int>, set<vector<char>>> pattern_learnts;

/// МАССИВ НОМЕРОВ ВХОДНЫХ ПЕРЕМЕННЫХ
vector<int> input_vars;

/// МАССИВ НОМЕРОВ ВЫХОДНЫХ ПЕРЕМЕННЫХ
vector<int> output_vars;

/// МНОЖЕСТВО НОМЕРОВ ВСЕХ ПЕРЕМЕННЫХ
set<int> all_vars_set;

/// МАССИВ НОМЕРОВ ВСЕХ ПЕРЕМЕННЫХ
vector<int> all_vars;

/// КОЛИЧЕСТВО КВАДРАТИЧНЫХ УРАВНЕНИЙ
int and_equations_cnt = 0;

/// КОЛИЧЕСТВО ВСЕХ ПЕРЕМЕННЫХ
int vars_cnt = 0;

/// КОЛИЧЕСТВО ВХОДНЫХ ПЕРЕМЕННЫХ
int input_vars_cnt = 0;

/// КОЛИЧЕСТВО ВЫХОДНЫХ ПЕРЕМЕННЫХ
int output_vars_cnt = 0;

/// СЧИТЫВАЕТСЯ В ЗАГОЛОВКЕ ФАЙЛА AIG, НЕ ИСПОЛЬЗУЕТСЯ
int latches_cnt = 0;


/// ЧТЕНИЕ ЗАГОЛОВКА AIG-ФАЙЛА
void read_header(istream &is)
{
	string header;
	is >> header;

	if (header == "aag") {
		is >> vars_cnt >> input_vars_cnt >> latches_cnt >> output_vars_cnt >> and_equations_cnt;
	}
	else {
		throw logic_error((string) "error: void read_header(): " +
			"wrong format: \'aag\' expected but \'" + header + "\' found");
	}
}

/// ЧТЕНИЕ СПИСКА ВХОДНЫХ ПЕРЕМЕННЫХ
void read_input(istream &is)
{
	input_vars.clear();
	input_vars.resize(input_vars_cnt);

	for (int i = 0; i < (int) input_vars_cnt; ++i) {
		is >> input_vars[i];
		all_vars_set.insert(input_vars[i] & -2);
	}
}

/// ЧТЕНИЕ СПИСКА ВЫХОДНЫХ ПЕРЕМЕННЫХ
void read_output(istream &is)
{
	output_vars.resize(output_vars_cnt);

	for (int i = 0; i < output_vars_cnt; ++i)
		is >> output_vars[i];
}

/// ЧТЕНИЕ СПИСКА КВАДРАТИЧНЫХ УРАВНЕНИЙ
void read_equations(istream &is)
{
	and_equations.resize(and_equations_cnt);
	for (int i = 0; i < and_equations_cnt; ++i) {
		int x, y, z;
		is >> x >> y >> z;
		and_equations[i] = {x, min(y, z), max(y, z)};
		all_vars_set.insert(x & -2);
	}
}

/// ЧТЕНИЕ AIG-ФАЙЛА
void read_aig(istream &is)
{
	try {
		read_header(is);
		read_input(is);
		read_output(is);
		read_equations(is);
	}
	catch (exception &e) {
		throw e;
	}
}

/// ЧТЕНИЕ СПИСКА ЛИНЕЙНЫХ УРАВНЕНИЙ
void read_linear_constraints(set<vector<int>> &linear_constraints, istream &is)
{
	string header;
	is >> header;
	
	if (header != "lin") {
		throw logic_error((string) "error: void read_linear_constraints(): " +
			"wrong format: \'lin\' expected but \'" + header + "\' found");
	}

	int linear_cnt;
	is >> linear_cnt;

	int line_cnt = 0;
	string line;
	stringstream ss;
	
	while (line_cnt < linear_cnt && getline(is, line)) {
		ss.clear();
		ss << line;

		int x, rem = 0;
		vector<int> equation;
		
		while (ss >> x) {
			equation.push_back(x & -2);
			rem ^= x & 1;
			all_vars_set.insert(x & -2);
		}

		if (equation.empty())
			continue;
		
		sort(equation.begin(), equation.end());
		equation[0] ^= rem;
		linear_constraints.insert(equation);
		++line_cnt;
	}

	if (linear_cnt != (int)linear_constraints.size())
		cerr << "warning: void read_linear_constraints(): " << "wrong linear constraints number: "
		     << linear_cnt << " expected but " << linear_constraints.size() << " found" << endl;
}

/// ЧТЕНИЕ assumptions
void read_assumptions(vector<int> &assumptions, istream &is)
{
	int x;
	
	while (is >> x)
		assumptions.push_back(x);
}

/// ДОБАВЛЕНИЕ ДИЗЪЮНКТА В ТАБЛИЦУ learnts.
/// ВОЗВРАЩАЕТ NOTHING_NEW, ЕСЛИ ТАКОЙ ДИЗЪЮНКТ УЖЕ БЫЛ В ТАБЛИЦЕ.
/// ИНАЧЕ ВОЗВРАЩАЕТ NEW_INFO.
Statuses add_learnts(map<vector<int>, set<vector<char>>> &learnts, vector<int> &key_value)
{
	sort(key_value.begin(), key_value.end());
	vector<int> key(key_value.size());
	vector<char> negations(key_value.size());

	for (int i = 0; i < (int) key_value.size(); ++i) {
		key[i] = key_value[i] & -2;
		negations[i] = key_value[i] & 1;
	}

	auto it = learnts.find(key);
	
	if (it == learnts.end()) {
		learnts[key].insert(negations);
		return NEW_INFO;
	}
	
	bool res = (it -> second).insert(negations).second;
	
	if (res)
		return NEW_INFO;
	else
		return NOTHING_NEW;
}

/// В res ЗАПИСЫВАЕТСЯ XOR-СУММА УРАВНЕНИЙ e1 И e2
Statuses equations_xor(vector<int> e1, vector<int> e2, vector<int> &res)
{
	char b = 0;
	
	if (!e1.empty()) {
		b ^= e1[0];
		e1[0] &= -2;
	}
	
	if (!e2.empty()) {
		b ^= e2[0];
		e2[0] &= -2;
	}
	
	b &= 1;
	set_symmetric_difference(e1.begin(), e1.end(), e2.begin(), e2.end(), back_inserter(res));
	
	if (b) {
		if (res.empty())
			return ERROR;
			// throw runtime_error("error: void equations_xor(): 0 == 1");
	
		res[0] ^= 1;
	}

	return NOTHING_NEW;
}

/// ОПРЕДЕЛЯЕТ ЗНАЧЕНИЕ ПЕРЕМЕНННОЙ var.
/// ВОЗВРАЩАЕТ NEW_INFO, ЕСЛИ ЗНАЧЕНИЕ ПЕРЕМЕННОЙ ДО ЭТОГО НЕ БЫЛО
/// ОПРЕДЕЛЕНО. ИНАЧЕ ВОЗВРАЩАЕТ 0.
Statuses define_variable_value(int var, char val, vector<char> &vars_values, vector<char> &is_def)
{
	if (is_def[var]) {
		if (vars_values[var] == val)
			return NOTHING_NEW;
		
		// throw runtime_error("error: void define_variable_value(): value equals to " +
		// 	to_string((int)val) + " but variable is already assigned to " +
		// 	to_string((int)vars_values[var]) + "\n");
		return ERROR;
	}

	is_def[var] = 1;
	is_def[var ^ 1] = 1;
	vars_values[var] = val;
	vars_values[var ^ 1] = (val ^ 1);

	return NEW_INFO;
}

/// ОПРЕДЕЛЯЕТ ЗНАЧЕНИЕ ПЕРЕМЕНННОЙ var.
/// ВОЗВРАЩАЕТ NEW_INFO, ЕСЛИ ЗНАЧЕНИЕ ПЕРЕМЕННОЙ ДО ЭТОГО НЕ БЫЛО
/// ОПРЕДЕЛЕНО. ИНАЧЕ ВОЗВРАЩАЕТ NOTHING_NEW.
Statuses define_variable_value(int var, char val,
		vector<char> &vars_values, vector<char> &is_def,
		const vector<int> &dsu)
{
	return define_variable_value(dsu[var], val, vars_values, is_def);
}

/// ОБЪЕДИНЕНИЕ КЛАССОВ ЭКВИВАЛЕНТНОСТИ, СОДЕРЖАЩИХ x И y.
/// В РАМКАХ РЕШЕНИЯ СИСТЕМЫ УРАВНЕНИЙ ЭТО ОЗНАЧАЕТ РАВЕНСТВО
/// ЗНАЧЕНИЙ ПЕРЕМЕННЫХ x И y.
/// ВОЗВРАЩАЕТ NEW_INFO, ЕСЛИ ПЕРЕМЕННЫЕ ДО ЭТОГО БЫЛИ В РАЗНЫХ
/// КЛАССАХ. ИНАЧЕ ВОЗВРАЩАЕТ NOTHING_NEW.
Statuses join_sets(int x, int y,
		vector<char> &vars_values, vector<char> &is_def,
		vector<int> &dsu, vector<vector<int>> &classes)
{
	x = dsu[x];
	y = dsu[y];

	if (x == y)
		return NOTHING_NEW;
	
	if (x == (y ^ 1))
		return ERROR;
		// throw runtime_error("error: void join_sets(): equation 0 = 1 has been deduced\n");
	
	if (is_def[x] && is_def[y]) {
		if (vars_values[x] != vars_values[y]) {
			return ERROR;
			// throw runtime_error("error: void join_sets(): equation 0 = 1 has been deduced\n");
		}

		return NOTHING_NEW;
	}

	if (is_def[x])
		return define_variable_value(y, vars_values[x], vars_values, is_def, dsu);

	if (is_def[y])
		return define_variable_value(x, vars_values[y], vars_values, is_def, dsu);

	if (classes[x].size() < classes[y].size())
		swap(x, y);

	for (int z: classes[y]) {
		dsu[z] = x;
		dsu[z ^ 1] = x ^ 1;
		classes[x].push_back(z);
		classes[x ^ 1].push_back(z ^ 1);
	}

	classes[y].clear();
	classes[y ^ 1].clear();

	return NEW_INFO;
}

/// ВЫВОД ИЗ КВАДРАТИЧНОГО УРАВНЕНИЯ.
/// ВОЗВРАЩАЕТ NEW_INFO, ЕСЛИ ХОТЬ ЧТО-ТО ВЫВЕЛОСЬ. ИНАЧЕ NOTHING_NEW.
Statuses propagation(const int ind,
		vector<char> &vars_values, vector<char> &is_def,
		vector<int> &dsu, vector<vector<int>> &classes,
		map<vector<int>, set<vector<char>>> &learnts,
		char &useless)
{
	useless = 1;
	
	auto e = and_equations[ind];
	int x = dsu[e.x];
	int y = dsu[e.y];
	int z = dsu[e.z];

	char val_x = vars_values[x];
	char val_y = vars_values[y];
	char val_z = vars_values[z];

	if (is_def[x] && is_def[y] && is_def[z])
		return NOTHING_NEW;

	if (z == y) {
		if (is_def[y])
			return define_variable_value(x, val_y, vars_values, is_def, dsu);

		if (is_def[x])
			return define_variable_value(y, val_x, vars_values, is_def, dsu);

		return join_sets(x, y, vars_values, is_def, dsu, classes);
	}

	if (z == (y ^ 1))
		return define_variable_value(x, 0, vars_values, is_def, dsu);

	if (y == x) {
		if (is_def[x] && val_x == 1)
			return define_variable_value(z, 1, vars_values, is_def, dsu);

		if (is_def[z] && val_z == 0)
			return define_variable_value(x, 0, vars_values, is_def, dsu);

		if (is_def[x])
			return NOTHING_NEW;

		if (is_def[z])
			return NOTHING_NEW;

		vector<int> key_value = {x ^ 1, z};
		// useless = 0; // TODO: убрать эту строчку
		return add_learnts(learnts, key_value);
	}

	if (y == (x ^ 1)) {
		int res1 = define_variable_value(x, 0, vars_values, is_def, dsu),
			res2 = define_variable_value(z, 0, vars_values, is_def, dsu);
		
		if (res1 == ERROR || res2 == ERROR)
			return ERROR;
		
		if (res1 == NEW_INFO || res2 == NEW_INFO)
			return NEW_INFO;
		
		return NOTHING_NEW;
	}

	if (z == x) {
		if (is_def[x] && val_x == 1)
			return define_variable_value(y, 1, vars_values, is_def, dsu);

		if (is_def[y] && val_y == 0)
			return define_variable_value(x, 0, vars_values, is_def, dsu);

		if (is_def[x])
			return NOTHING_NEW;

		if (is_def[y])
			return NOTHING_NEW;

		vector<int> key_value = {x ^ 1, y};
		// useless = 0; // TODO: убрать эту строчку
		return add_learnts(learnts, key_value);
	}

	if (z == (x ^ 1)) {
		int res1 = define_variable_value(x, 0, vars_values, is_def, dsu),
			res2 = define_variable_value(y, 0, vars_values, is_def, dsu);
		
		if (res1 == ERROR || res2 == ERROR)
			return ERROR;
		
		if (res1 == NEW_INFO || res2 == NEW_INFO)
			return NEW_INFO;
		
		return NOTHING_NEW;
	}

	if (!is_def[x]) {
		if ((is_def[y] && val_y == 0) || (is_def[z] && val_z == 0))
			return define_variable_value(x, 0, vars_values, is_def, dsu);

		if (is_def[y] && is_def[z]) // && val_y == 1 && val_z == 1
			return define_variable_value(x, 1, vars_values, is_def, dsu);
			
		if (is_def[y]) // && val_y == 1 && !is_def[z]
			return join_sets(x, z, vars_values, is_def, dsu, classes);

		if (is_def[z]) // && val_z == 1 && !is_def[y]
			return join_sets(x, y, vars_values, is_def, dsu, classes);

		useless = 0;
		return NOTHING_NEW;
	}

	if (val_x == 0) { // is_def[x]
		if (is_def[y] && val_y == 1) // && !is_def[z]
			return define_variable_value(z, 0, vars_values, is_def, dsu);

		if (is_def[z] && val_z == 1) // && !is_def[y]
			return define_variable_value(y, 0, vars_values, is_def, dsu);

		vector<int> key_value = {y ^ 1, z ^ 1};
		useless = 0; // TODO: убрать эту строчку
		return add_learnts(learnts, key_value);
	}

	// val_x == 1
	int res1 = define_variable_value(y, 1, vars_values, is_def, dsu),
		res2 = define_variable_value(z, 1, vars_values, is_def, dsu);
	
	if (res1 == ERROR || res2 == ERROR)
		return ERROR;
	
	if (res1 == NEW_INFO || res2 == NEW_INFO)
		return NEW_INFO;
	
	return NOTHING_NEW;
}

/// ВЫВОД ИЗ КВАДРАТИЧНОГО УРАВНЕНИЯ.
/// ПРОВЕРКА СОВПАДЕНИЯ ПАР ВХОДОВ.
/// ВОЗВРАЩАЕТ NEW_INFO, ЕСЛИ ХОТЬ ЧТО-ТО ВЫВЕЛОСЬ. ИНАЧЕ NOTHING_NEW.
Statuses propagation(const int ind,
		vector<char> &vars_values, vector<char> &is_def,
		vector<int> &dsu, vector<vector<int>> &classes,
		map<pair<int, int>, int> &gate_pairs,
		map<vector<int>, set<vector<char>>> &learnts,
		set<vector<int>> &linear_constraints, char &useless)
{
	auto e = and_equations[ind];
	int x = dsu[e.x];
	int y = dsu[e.y];
	int z = dsu[e.z];

	if (is_def[x] && is_def[y] && is_def[z]) {
		useless = 1;
		return NOTHING_NEW;
	}

	useless = 0;

	if (y > z)
		swap(y, z);

	pair<int, int> key = {y & -2, z & -2};

	auto it = gate_pairs.find(key);
	int res = NOTHING_NEW;

	if (it == gate_pairs.end()) {
		gate_pairs[key] = ind;
	}
	else if (it -> second != ind) {
		int j = it -> second;
		auto f = and_equations[j];
		int _x = dsu[f.x], _y = dsu[f.y], _z = dsu[f.z];

		if (_y > _z)
			swap(_y, _z);

		int id = ((y & 1) << 1) ^ (z & 1);
		int dif = ((_y & 1) << 1) ^ (_z & 1) ^ id;

		if (dif == 0) { // x +_x = yz + yz = 0
			if (_x != x) {
				res = join_sets(x, _x, vars_values, is_def, dsu, classes);
				
				if (res == ERROR)
					return ERROR;
				
				useless = 1;
			}
		}
		else {
			vector<int> lin;

			if (dif == 1) // x + _x = yz + y(z + 1) = yz + yz + y = y
				lin = {x, _x, y};
			else if (dif == 2) // x + _x = yz + (y + 1)z = yz + z + yz = z
				lin = {x, _x, z};
			else // dif == 3, x + _x = yz + (y + 1)(z + 1) = yz + yz + y + z + 1 = y + (z + 1)
				lin = {x, _x, y, z ^ 1};

			int r = 0;
			
			for (auto &var: lin) {
				r ^= var & 1;
				var &= -2;
			}

			sort(lin.begin(), lin.end());
			lin[0] ^= r;

			if (linear_constraints.insert(lin).second)
				res = NEW_INFO;

			useless = 1;
		}
	}

	char u;
	int res1 = propagation(ind, vars_values, is_def, dsu, classes, learnts, u);
	useless |= u;

	if (res1 == ERROR)
		return ERROR;
	
	if (res == NEW_INFO || res1 == NEW_INFO)
		return NEW_INFO;
	
	return NOTHING_NEW;
}

/// ВЫВОД ИЗ ГРУППЫ ДИЗЪЮНКТОВ НАД ОДНИМ МНОЖЕСТВОМ ПЕРЕМЕННЫХ key.
/// ВОЗВРАЩАЕТ NEW_INFO, ЕСЛИ ХОТЬ ЧТО-ТО ВЫВЕЛОСЬ. ИНАЧЕ NOTHING_NEW.
Statuses learnts_propagation(vector<int> &key, vector<vector<char>> &negations,
		vector<char> &vars_values, vector<char> &is_def,
		vector<int> &dsu, vector<vector<int>> &classes,
		char &useless)
{
	useless = 1;
	int n = key.size();
	vector<vector<int>> disjuncts;
	vector<int> variables = key;
	for (auto &x: variables)
		x = dsu[x];
	for (auto &v: negations) {
		vector<int> disjunct;
		bool skip = 0; // applying UP rule flag
		for (int i = 0; i < (int) key.size(); ++i) {
			int x = variables[i] ^ v[i];
			if (is_def[x]) {
				if (vars_values[x] == 0)
					continue;
				// vars_values[x] == 1
				skip = 1;
				break;
			}
			disjunct.push_back(x);
		}
		if (skip)
			continue;
		disjuncts.push_back(disjunct);
	}

	if (disjuncts.empty())
		return NOTHING_NEW;

	for (auto x: variables) {
		if (is_def[x])
			--n;
	}

	if (n == 0) {
		// std::cerr << "error: char learnts_propagation(): empty disjunct can't be solved\n"; // TODO: throw runtime_error("...")
		return ERROR;
	}
	else if (n == 1) {
		int res;

		for (auto &d: disjuncts) {
			int x = dsu[d[0]];
			int res1 = define_variable_value(x, 1, vars_values, is_def, dsu);

			if (res1 == ERROR)
				return ERROR;
			
			if (res1 == NEW_INFO)
				res = NEW_INFO;
		}

		if (res == NEW_INFO)
			return NEW_INFO;
		
		return NOTHING_NEW;
	}
	else if (n == 2) {
		if (disjuncts.size() == 1) {
			auto d = disjuncts[0];
			int x = dsu[d[0]], y = dsu[d[1]];

			if (x == y) {
				return define_variable_value(x, 1, vars_values, is_def, dsu);
			}
			else if (x == (y ^ 1)) {
				return NOTHING_NEW;
			}
			else {
				useless = 0;
				return NOTHING_NEW;
			}
		}
		else if (disjuncts.size() == 2) {
			auto d0 = disjuncts[0], d1 = disjuncts[1];
			int x1 = dsu[d0[0]], y1 = dsu[d0[1]],
				x2 = dsu[d1[0]], y2 = dsu[d1[1]];
			
			if (x1 == x2)
				return define_variable_value(x1, 1, vars_values, is_def, dsu);
			else if (y1 == y2)
				return define_variable_value(y1, 1, vars_values, is_def, dsu);
			else if (x1 != (y1 ^ 1))
				return join_sets(x1, y1 ^ 1, vars_values, is_def, dsu, classes);
			else
				return NOTHING_NEW;
		}
		else if (disjuncts.size() == 3) {
			int x = 0, y = 0;

			for (auto &d: disjuncts) {
				x ^= dsu[d[0]];
				y ^= dsu[d[1]];
			}

			int res1 = define_variable_value(x, 0, vars_values, is_def, dsu),
				res2 = define_variable_value(y, 0, vars_values, is_def, dsu);
			
			if (res1 == ERROR || res2 == ERROR)
				return ERROR;
			
			if (res1 == NEW_INFO || res2 == NEW_INFO)
				return NEW_INFO;
			
			return NOTHING_NEW;
		}
		else {
			// cerr << "error: char learnts_propagation(): " <<
			// 	"4 different disjuncts in 2 variables can't be solved\n"; // TODO: throw runtime_error("...")
			return ERROR;
		}
	}
	else { // n >= 3
		// clog << "warning: void learnts_propagation(): n >= 3. There are no methods to use it.\n"; // TODO: throw smth
		useless = 0;
		return NOTHING_NEW;
	}
	
	return NOTHING_NEW;
}

/// ПОДСТАНОВКА НОВОЙ ИНФОРМАЦИИ В СИСТЕМУ ДИЗЪЮНКТОВ.
/// ВОЗВРАЩАЕТ NEW_INFO, ЕСЛИ ХОТЬ ЧТО-ТО ВЫВЕЛОСЬ. ИНАЧЕ NOTHING_NEW.
Statuses analyze_learnts(map<vector<int>, set<vector<char>>> &learnts,
		vector<char> &vars_values, vector<char> &is_def,
		vector<int> &dsu, vector<vector<int>> &classes)
{
	int res = NOTHING_NEW;

	for (auto it = learnts.begin(); it != learnts.end(); ) {
		auto key = it -> first;
		vector<vector<char>> negations((it -> second).begin(), (it -> second).end());
		bool change_key = 0;

		for (int i = 0; i < (int) key.size(); ++i) {
			int x = key[i];

			if (dsu[x] != x) {
				change_key = 1;
				key[i] = dsu[x] & -2;

				if (dsu[x] & 1) {
					for (auto &v: negations)
						v[i] ^= 1;
				}
			}
		}

		if (change_key) {
			learnts[key].insert(negations.begin(), negations.end());
			it = learnts.erase(it);
			res = NEW_INFO;
			continue;
		}

		char useless;
		int res1 = learnts_propagation(key, negations, vars_values, is_def, dsu, classes, useless);
		
		if (res1 == ERROR)
			return ERROR;
		
		if (res1 == NEW_INFO)
			res = NEW_INFO;

		if (useless)
			it = learnts.erase(it);
		else
			++it;
	}

	if (res == NEW_INFO)
		return NEW_INFO;
	
	return NOTHING_NEW;
}

/// ПРОСТАЯ ПОДСТАНОВКА НОВОЙ ИНФОРМАЦИИ В ЛИНЕЙНУЮ СИСТЕМУ.
/// НОВАЯ ВЫВЕДЕННАЯ ИНФОРМАЦИЯ СОХРАНЯЕТСЯ В relations.
Statuses simple_linear_propagation(set<vector<int>> &linear_constraints,
		vector<vector<int>> &relations,
		vector<char> &vars_values, vector<char> &is_def,
		vector<int> &dsu)
{
	vector<vector<int>> changes;

	for (auto it = linear_constraints.begin(); it != linear_constraints.end(); ) {
		char useless = 0, value = 0, change = 1;
		vector<int> equation_vector;
		map<int, int> equation_map;

		for (auto x: *it) {
			if (x != dsu[x])
				change = 1;
			
			x = dsu[x];

			if (is_def[x]) {
				value ^= vars_values[x];
				continue;
			}

			value ^= x & 1;
			++equation_map[x & -2];
		}

		for (auto &p: equation_map) {
			if (p.second > 1)
				change = 1;
			
			if (p.second & 1) {
				equation_vector.push_back(p.first ^ value);
				value = 0;
			}
		}

		if (equation_vector.empty()) {
			if (value) {
				// cerr << "error: void simple_linear_propagation(): " <<
				// 	"wrong equation has been deduced: 0 = 1\n"; // TODO: throw runtime_error(...)
				return ERROR;
			}

			useless = 1;
		}
		else if (equation_vector.size() <= 2) {
			relations.push_back(equation_vector);
			useless = 1;
		}

		if (useless) {
			it = linear_constraints.erase(it);
			continue;
		}
		else if (change) {
			changes.push_back(equation_vector);
			it = linear_constraints.erase(it);
			continue;
		}
		else {
			++it;
		}
	}

	linear_constraints.insert(changes.begin(), changes.end());

	return NOTHING_NEW;
}

/// ПОПЫТКА РЕШЕНИЯ СЛАУ. МОЖЕТ БЫТЬ ВЫВЕДЕНА ДОПОЛНИТЕЛЬНАЯ
/// ИНФОРМАЦИЯ, ЕСЛИ СИСТЕМА НЕДООПРЕДЕЛЕНА.
/// НОВАЯ ВЫВЕДЕННАЯ ИНФОРМАЦИЯ СОХРАНЯЕТСЯ В relations.
Statuses linear_propagation(set<vector<int>> &linear_constraints,
		vector<vector<int>> &relations)
{
	vector<vector<int>> equations_by_var(vars_cnt + 1);
	int counter = 0;

	/// Gauss algorithm stage 1
	for (auto it = linear_constraints.begin(); it != linear_constraints.end(); ++it) {
		for (int i = 1; i < (int)(*it).size(); ++i)
			equations_by_var[(*it)[i] / 2].push_back(counter);
		
		++counter;
		auto it1 = it;
		++it1;

		while (it1 != linear_constraints.end() && ((*it1)[0] / 2) == ((*it)[0] / 2)) {
			vector<int> res;

			if (equations_xor(*it, *it1, res) == ERROR)
				return ERROR;

			if (!res.empty())
				linear_constraints.insert(res);
			
			it1 = linear_constraints.erase(it1);
		}
	}
	
	/// СОХРАНИТЬ СИСТЕМУ В vector<vector<int>> ls
	/// ДЛЯ КАЖДОГО x \in ls СОХРАНИТЬ ВСЕ УРАВНЕНИЯ, СОДЕРЖАЩИЕ x[0] или x[0] ^ 1
	/// ИСПОЛЬЗОВАТЬ vector<vector<int>> equations_by_vars РАЗМЕРА vars_cnt + 1

	vector<vector<int>> ls(linear_constraints.begin(), linear_constraints.end());

	/// Gauss algorithm stage 2
	for (int i = ls.size() - 1; i >= 0; --i) {
		/// ЕСЛИ ls[i] СОДЕРЖИТ ЛИНЕЙНОЕ СООТНОШЕНИЕ
		/// НАД 1 ИЛИ 2 ПЕРЕМЕНЫМИ, НАДО ЕГО СОХРАНИТЬ
		if (ls[i].size() <= 2)
			relations.push_back(ls[i]);

		for (int j : equations_by_var[ls[i][0] / 2]) {
			vector<int> res;
			equations_xor(ls[i], ls[j], res);
			ls[j] = res;
			if (ls[j].size() <= 2)
				relations.push_back(ls[j]);
		}
	}
	
	linear_constraints = set<vector<int>>(ls.begin(), ls.end());

	return NOTHING_NEW;
}

/// ПРИМЕНЕНИЕ ПОЛУЧЕННОЙ ИНФОРМАЦИИ ИЗ relations, КОТОРАЯ
/// НЕ МОГЛА БЫТЬ ПРИМЕНЕНА НЕПОСРЕДСТВЕННО ВО ВРЕМЯ ВЫВОДА.
/// ВОЗВРАЩАЕТ NEW_INFO, ЕСЛИ ХОТЬ ЧТО-ТО ВЫВЕЛОСЬ. ИНАЧЕ NOTHING_NEW.
Statuses analyze_relations(vector<vector<int>> &relations,
		vector<char> &vars_values, vector<char> &is_def,
		vector<int> &dsu, vector<vector<int>> &classes)
{
	if (relations.empty())
		return NOTHING_NEW;
	
	int res = NOTHING_NEW;

	for (auto &relation: relations) {
		if (relation.size() == 1) {
			int res1 = define_variable_value(relation[0], 0, vars_values, is_def, dsu);

			if (res1 == ERROR)
				return ERROR;
			
			if (res1 == NEW_INFO)
				res = NEW_INFO;
		}
		else if (relation.size() == 2) {
			int res1 = join_sets(relation[0], relation[1], vars_values, is_def, dsu, classes);

			if (res1 == ERROR)
				return ERROR;
			
			if (res1 == NEW_INFO)
				res = NEW_INFO;
		}
	}

	if (res == NEW_INFO)
		return NEW_INFO;
	
	return NOTHING_NEW;
}

/// ВЫВОД ПО ВСЕМ КВАДРАТИЧНЫМ УРАВНЕНИЯМ. ИСПОЛЬЗУЮТСЯ
/// УСЛОЖНЁННЫЕ ПРАВИЛА ВЫВОДА (ДЛЯ ФУНКЦИИ solve).
/// ВОЗВРАЩАЕТ NEW_INFO, ЕСЛИ ХОТЬ ЧТО-ТО ВЫВЕЛОСЬ. ИНАЧЕ NOTHING_NEW.
Statuses analyze_equations(vector<char> &vars_values, vector<char> &is_def,
		vector<int> &dsu, vector<vector<int>> &classes,
		map<pair<int, int>, int> &gate_pairs,
		map<vector<int>, set<vector<char>>> &learnts,
		set<vector<int>> &linear_constraints,
		vector<char> &useless_equations)
{
	int res = NOTHING_NEW;

	for (int i = 0; i < and_equations_cnt; ++i) {
		if (useless_equations[i])
			continue;

		char useless;
		int res1 = propagation(i, vars_values, is_def,
			dsu, classes, gate_pairs, learnts,
			linear_constraints, useless);
		
		if (res1 == ERROR)
			return ERROR;
		
		if (res1 == NEW_INFO)
			res = NEW_INFO;
		
		if (useless)
			useless_equations[i] = 1;
	}

	if (res == NEW_INFO)
		return NEW_INFO;

	return NOTHING_NEW;
}

/// ВЫВОД ПО ВСЕМ КВАДРАТИЧНЫМ УРАВНЕНИЯМ. ИСПОЛЬЗУЮТСЯ
/// ПРОСТЫЕ ПРАВИЛА ВЫВОДА (ДЛЯ ФУНКЦИИ find_output).
/// ВОЗВРАЩАЕТ NEW_INFO, ЕСЛИ ХОТЬ ЧТО-ТО ВЫВЕЛОСЬ. ИНАЧЕ NOTHING_NEW.
Statuses analyze_equations(vector<char> &vars_values, vector<char> &is_def,
		vector<int> &dsu, vector<vector<int>> &classes,
		map<vector<int>, set<vector<char>>> &learnts,
		vector<char> &useless_equations)
{
	int res = NOTHING_NEW;

	for (int i = 0; i < and_equations_cnt; ++i) {
		if (useless_equations[i])
			continue;

		char useless;
		int res1 = propagation(i, vars_values, is_def,
			dsu, classes, learnts, useless);
		
		if (res1 == ERROR)
			return ERROR;
		
		if (res1 == NEW_INFO)
			res = NEW_INFO;
		
		if (useless)
			useless_equations[i] = 1;
	}

	if (res == NEW_INFO)
		return NEW_INFO;

	return NOTHING_NEW;
}

/// УПРОЩЕНИЕ СИСТЕМЫ УРАВНЕНИЙ. ПРОИСХОДИТ ИТЕРАТИВНОЕ ПРИМЕНЕНИЕ
/// ПРАВИЛ ВЫВОДА, ПОКА ВЫВОДИТСЯ НОВАЯ ИНФОРМАЦИЯ.
/// СТРУКТУРУ ФУНКЦИИ (КОМБИНАЦИЮ ПРАВИЛ ВЫВОДА) МОЖНО МЕНЯТЬ.
Statuses simplify(vector<char> &vars_values, vector<char> &is_def,
		vector<int> &dsu, vector<vector<int>> &classes,
		vector<char> &useless_equations,
		set<vector<int>> &linear_constraints,
		map<vector<int>, set<vector<char>>> &learnts)
{
	/// ТАБЛИЦА И-ГЕЙТОВ С ОДИНАКОВЫМИ ПАРАМИ ПЕРЕМЕННЫХ НА ВХОДЕ.
	/// КЛЮЧ - ПАРА ПЕРЕМЕННЫХ; ЗНАЧЕНИЕ - НОМЕР ГЕЙТА
	map<pair<int, int>, int> gate_pairs;

	while (true) {
		int res = NOTHING_NEW;
		
		while (true) {
			res = NOTHING_NEW;
			
			int res1 = analyze_equations(vars_values, is_def, dsu, classes,
				gate_pairs, learnts, linear_constraints, useless_equations);
			
			if (res1 == ERROR)
				return ERROR;
			
			if (res1 == NEW_INFO)
				res = NEW_INFO;
			
			vector<vector<int>> relations;

			res1 = simple_linear_propagation(linear_constraints, relations, vars_values, is_def, dsu);

			if (res1 == ERROR)
				return ERROR;
			
			if (res1 == NEW_INFO)
				res = NEW_INFO;

			res1 = analyze_relations(relations, vars_values, is_def, dsu, classes);

			if (res1 == ERROR)
				return ERROR;
			
			if (res1 == NEW_INFO)
				res = NEW_INFO;

			if (res == NOTHING_NEW)
				break;
		}

		res = analyze_learnts(learnts, vars_values, is_def, dsu, classes);

		if (res == ERROR)
			return ERROR;

		if (res == NOTHING_NEW) {
			vector<vector<int>> relations;
			auto linear_constraints_copy = linear_constraints;
			linear_propagation(linear_constraints_copy, relations);
			res = analyze_relations(relations, vars_values, is_def, dsu, classes);

			if (res == ERROR)
				return ERROR;
		}

		if (res == NOTHING_NEW)
			break;
	}

	for (auto x: all_vars) {
		if (!is_def[dsu[x]])
			return UNSOLVED;
	}

	return SOLVED;
}

/// ПРИМЕНЕНИЕ ПРДСТАНОВКИ И ВЫВОД НОВОЙ СИСТЕМЫ УРАВНЕНИЙ.
/// ВЫВОДЯТСЯ НОВЫЕ СИСТЕМА КВАДРАТИЧНЫХ УРАВНЕНИЙ, СИСТЕМА
/// ЛИНЕЙНЫХ УРАВНЕНИЙ, СПИСОК ДИЗЪЮНКТОВ.
Statuses apply_substitution(const vector<int> &assumptions, vector<char> &answer)
{
	vector<char> vars_values(2 * (vars_cnt + 1), 0),
		is_def(2 * (vars_cnt + 1), 0);
	vector<int> dsu(2 * (vars_cnt + 1));
	vector<vector<int>> classes(2 * (vars_cnt + 1));
	vector<char> useless_equations(and_equations_cnt, 0);
	auto linear_constraints = pattern_linear_constraints;
	auto learnts = pattern_learnts;

	for (int i = 0; i < (int)dsu.size(); ++i) {
		dsu[i] = i;
		classes[i].push_back(i);
	}

	for (auto x: assumptions) {
		int res = define_variable_value(x, 0, vars_values, is_def, dsu);

		if (res == ERROR)
			return ERROR;
	}

	int res = simplify(vars_values, is_def, dsu, classes, useless_equations,
		linear_constraints, learnts);

	if (res == ERROR)
		return ERROR;

	if (res == SOLVED) {
		answer.resize(2 * vars_cnt + 2);
		for (int x = 0; x < 2 * vars_cnt + 2; ++x)
			answer[x] = vars_values[dsu[x]];
		
		return SOLVED;
	}

	return UNSOLVED;
}


pair<int, vector<char>> propagate(const vector<int> &assumptions)
{
	vector<char> answer;

	int status = apply_substitution(assumptions, answer);

	return {status, answer};
}


int main()
{
	
	vector<int> assumptions;
	
	try {
		read_aig(cin);

		read_linear_constraints(pattern_linear_constraints, cin);
		
		read_assumptions(assumptions, cin);
	}
	catch (exception &e) {
		cerr << e.what() << endl;
		
		return 0;
	}
	
	all_vars = vector<int>(all_vars_set.begin(), all_vars_set.end());
	
	pair<int, vector<char>> result = propagate(assumptions);
	
	if (result.first == (int) SOLVED) {
		for (auto x: all_vars)
			cout << (x ^ result.second[x]) << " ";
		
		return 10;
	}
	else if (result.first == (int) UNSOLVED)
		return 20;
	
	return 0;

}
